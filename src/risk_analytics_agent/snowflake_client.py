"""Singleton Snowflake connection manager with OAuth support."""

from __future__ import annotations

import logging
import threading

import requests
import snowflake.connector

from risk_analytics_agent.config import load_snowflake_config

logger = logging.getLogger(__name__)


def _refresh_oauth_token(cfg: dict) -> str:
    """Fetch a fresh OAuth token from the token endpoint.

    Only called when ``token_endpoint``, ``client_id``, and
    ``client_secret`` are all present in the config.
    """
    resp = requests.post(
        cfg["token_endpoint"],
        data={
            "grant_type": "client_credentials",
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "scope": cfg.get("scope", ""),
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


class SnowflakeClient:
    """Lazy-connecting, auto-reconnecting Snowflake client (singleton)."""

    _instance: SnowflakeClient | None = None
    _lock = threading.Lock()

    def __new__(cls) -> SnowflakeClient:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connection = None
                cls._instance._config = None
            return cls._instance

    def _get_config(self) -> dict:
        if self._config is None:
            self._config = load_snowflake_config()
        return self._config
    
    def _is_configured(self) -> bool:
        """Check if Snowflake credentials are properly configured."""
        cfg = self._get_config()
        required_fields = ["account", "user"]
        return all(cfg.get(field) and cfg[field].strip() for field in required_fields)

    def _resolve_token(self, cfg: dict) -> str:
        """Return an OAuth token, refreshing from the endpoint if configured."""
        if cfg.get("token_endpoint") and cfg.get("client_id") and cfg.get("client_secret"):
            logger.info("Refreshing OAuth token from %s", cfg["token_endpoint"])
            return _refresh_oauth_token(cfg)
        return cfg["token"]

    def _connect(self) -> snowflake.connector.SnowflakeConnection:
        cfg = self._get_config()
        
        # Check if we're in demo mode (no credentials configured)
        if not self._is_configured():
            raise ConnectionError(
                "Snowflake credentials not configured. "
                "Please set SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, and other required "
                "environment variables, or use the mock tools for demo mode. "
                "See DEMO_TOOLS_GUIDE.md for mock data usage."
            )
        
        token = self._resolve_token(cfg)
        logger.info("Connecting to Snowflake account=%s via OAuth", cfg.get("account"))
        conn = snowflake.connector.connect(
            account=cfg["account"],
            user=cfg["user"],
            authenticator=cfg.get("authenticator", "oauth"),
            token=token,
            warehouse=cfg.get("warehouse"),
            database=cfg.get("database"),
            schema=cfg.get("schema"),
            role=cfg.get("role"),
        )
        return conn

    @property
    def connection(self) -> snowflake.connector.SnowflakeConnection:
        """Get an active connection, reconnecting if needed."""
        if self._connection is None or self._connection.is_closed():
            self._connection = self._connect()
        return self._connection

    def execute(self, sql: str, params: dict | None = None) -> list[dict]:
        """Execute a SQL query and return results as a list of dicts.
        
        Raises:
            ConnectionError: If Snowflake is not configured (demo mode)
        """
        if not self._is_configured():
            raise ConnectionError(
                "Snowflake not configured. Use mock tools instead: "
                "generate_mock_liquidity_data, generate_variance_analysis, etc."
            )
        
        cursor = self.connection.cursor(snowflake.connector.DictCursor)
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def close(self) -> None:
        """Close the Snowflake connection."""
        if self._connection and not self._connection.is_closed():
            self._connection.close()
            self._connection = None

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton (for testing)."""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.close()
                cls._instance = None


def get_client() -> SnowflakeClient:
    """Get the singleton SnowflakeClient instance."""
    return SnowflakeClient()
