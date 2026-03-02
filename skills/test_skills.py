"""
Test script to verify Skills are loading correctly in the Risk Analytics Agent.

Run this to validate your Skills implementation before deploying.
"""

import pathlib
import sys

from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset


def test_skill_loading():
    """Test that skills can be loaded from directories."""
    
    print("=" * 70)
    print("Testing Google ADK Skills Implementation")
    print("=" * 70)
    
    # Get project root
    project_root = pathlib.Path(__file__).parent.parent
    skills_dir = project_root / "skills"
    
    print(f"\n📁 Skills directory: {skills_dir}")
    print(f"   Exists: {skills_dir.exists()}")
    
    if not skills_dir.exists():
        print("❌ Skills directory not found!")
        return False
    
    # Test each skill
    skills_to_test = [
        ("mlo_analysis", "MLO Analysis Skill"),
        ("anomaly_detection", "Anomaly Detection Skill"),
    ]
    
    loaded_skills = []
    
    for skill_name, display_name in skills_to_test:
        print(f"\n{'─' * 70}")
        print(f"Testing: {display_name}")
        print(f"{'─' * 70}")
        
        skill_path = skills_dir / skill_name
        print(f"Path: {skill_path}")
        
        # Check if skill directory exists
        if not skill_path.exists():
            print(f"❌ Skill directory not found: {skill_path}")
            continue
        
        # Check for SKILL.md
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            print(f"❌ SKILL.md not found in {skill_path}")
            continue
        
        print(f"✅ SKILL.md found")
        
        # Check for references directory
        refs_dir = skill_path / "references"
        if refs_dir.exists():
            ref_files = list(refs_dir.glob("*.md"))
            print(f"✅ References directory found ({len(ref_files)} files)")
            for ref in ref_files:
                print(f"   - {ref.name}")
        
        # Check for assets directory
        assets_dir = skill_path / "assets"
        if assets_dir.exists():
            asset_files = list(assets_dir.glob("*"))
            print(f"✅ Assets directory found ({len(asset_files)} files)")
            for asset in asset_files:
                print(f"   - {asset.name}")
        
        # Try to load the skill
        try:
            print(f"\n⏳ Loading skill...")
            skill = load_skill_from_dir(skill_path)
            print(f"✅ Skill loaded successfully!")
            
            # Display skill metadata
            print(f"\n📋 Skill Metadata:")
            print(f"   Name: {skill.frontmatter.name}")
            print(f"   Description: {skill.frontmatter.description}")
            if hasattr(skill.frontmatter, 'version'):
                print(f"   Version: {skill.frontmatter.version}")
            if hasattr(skill.frontmatter, 'tags') and skill.frontmatter.tags:
                print(f"   Tags: {', '.join(skill.frontmatter.tags)}")
            
            # Check instructions
            if skill.instructions:
                lines = skill.instructions.strip().split('\n')
                print(f"\n📝 Instructions: {len(lines)} lines")
                print(f"   Preview: {lines[0][:60]}...")
            
            # Check resources
            if skill.resources:
                if skill.resources.references:
                    print(f"\n📚 References: {len(skill.resources.references)} items")
                    for ref_name in skill.resources.references.keys():
                        print(f"   - {ref_name}")
                
                if skill.resources.assets:
                    print(f"\n🗂️  Assets: {len(skill.resources.assets)} items")
                    for asset_name in skill.resources.assets.keys():
                        print(f"   - {asset_name}")
            
            loaded_skills.append(skill)
            
        except Exception as e:
            print(f"❌ Failed to load skill: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Test creating a SkillToolset
    if loaded_skills:
        print(f"\n{'=' * 70}")
        print("Testing SkillToolset Creation")
        print(f"{'=' * 70}")
        
        try:
            toolset = skill_toolset.SkillToolset(skills=loaded_skills)
            print(f"✅ SkillToolset created successfully with {len(loaded_skills)} skills")
            print(f"   Toolset name: {toolset.name if hasattr(toolset, 'name') else 'N/A'}")
        except Exception as e:
            print(f"❌ Failed to create SkillToolset: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Summary
    print(f"\n{'=' * 70}")
    print("Summary")
    print(f"{'=' * 70}")
    print(f"✅ Skills loaded: {len(loaded_skills)}/{len(skills_to_test)}")
    
    if len(loaded_skills) == len(skills_to_test):
        print("\n🎉 All tests passed! Skills are ready to use.")
        return True
    else:
        print(f"\n⚠️  Some skills failed to load. Check errors above.")
        return False


def test_agent_imports():
    """Test that agents with skills can be imported."""
    
    print(f"\n{'=' * 70}")
    print("Testing Agent Imports")
    print(f"{'=' * 70}")
    
    try:
        print("\n⏳ Importing variance_analysis_agent...")
        from risk_analytics_agent.sub_agents.variance_analysis.agent import (
            variance_analysis_agent,
        )
        print(f"✅ Imported successfully")
        print(f"   Agent name: {variance_analysis_agent.name}")
        print(f"   Tools count: {len(variance_analysis_agent.tools)}")
        
    except Exception as e:
        print(f"❌ Failed to import variance_analysis_agent: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        print("\n⏳ Importing anomaly_detection_agent...")
        from risk_analytics_agent.sub_agents.anomaly_detection.agent import (
            anomaly_detection_agent,
        )
        print(f"✅ Imported successfully")
        print(f"   Agent name: {anomaly_detection_agent.name}")
        print(f"   Tools count: {len(anomaly_detection_agent.tools)}")
        
    except Exception as e:
        print(f"❌ Failed to import anomaly_detection_agent: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"\n🎉 All agent imports successful!")
    return True


def main():
    """Run all tests."""
    
    print("\n" + "🔍 " * 35)
    print(" " * 25 + "ADK Skills Validation")
    print("🔍 " * 35 + "\n")
    
    # Test 1: Skill loading
    skills_ok = test_skill_loading()
    
    # Test 2: Agent imports (only if skills loaded successfully)
    if skills_ok:
        agents_ok = test_agent_imports()
    else:
        print("\n⚠️  Skipping agent import tests due to skill loading failures")
        agents_ok = False
    
    # Final summary
    print(f"\n{'=' * 70}")
    print("Final Results")
    print(f"{'=' * 70}")
    
    if skills_ok and agents_ok:
        print("✅ All tests passed!")
        print("\n✨ Your Skills implementation is working correctly.")
        print("   You can now use Skills in your agents.")
        return 0
    else:
        print("❌ Some tests failed")
        print("\n🔧 Please fix the errors above before using Skills.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
