# CLAUDE.md - Project Context for AI Assistant

## Addressing the User
Greetings, Jedi Master. This document serves as context for AI assistants working on this project.

## Project Overview
This project facilitates the migration and optimization of digital assets from iCloud to Google Drive, with intelligent deduplication and backup verification capabilities.

## Project Purpose

### Primary Goal
Build a Python-based system to:
1. **Extract** photos and other assets from iCloud
2. **Transfer** files to Google Drive using cloud-based infrastructure
3. **Optimize** the network efficiency by leveraging a cloud box for fast transfers
4. **Reduce** filesets using AI tooling from multiple cloud providers (Google, Amazon)
5. **Verify** against existing local drive backups to prevent duplication

### Architecture Approach
- **Language**: Python (primary)
- **Infrastructure**: Cloud box for network-optimized transfers
- **AI Integration**: 
  - Google Cloud AI services
  - Amazon AWS AI services
- **Storage Platforms**:
  - Source: iCloud
  - Destination: Google Drive
  - Verification: Local drive backups

### Key Workflows
1. **Extraction Phase**: Pull files from iCloud API/storage
2. **Transfer Phase**: Move assets to Google Drive via cloud box
3. **AI Processing Phase**: Use Google/AWS AI to analyze and deduplicate files
4. **Verification Phase**: Cross-reference against local backup inventory
5. **Optimization Phase**: Remove duplicates and optimize storage

## Technical Considerations
- Network optimization via cloud box infrastructure
- API integration with iCloud, Google Drive, Google Cloud AI, AWS AI
- Backup verification logic to prevent data loss
- Deduplication algorithms leveraging AI capabilities

## Library Decisions

### iCloud Access
- **Primary**: `pyicloud` - For metadata listing, selective control, and flexible Python scripting
  - Actively maintained (latest: January 2026)
  - Full API access to photos, files, and other iCloud services
  - Supports 2FA authentication
  - Best for programmatic metadata extraction and selective operations
  
- **Secondary**: `icloudpd` - Reserved for bulk photo downloads when needed
  - Specialized CLI tool for mass photo library downloads
  - Excellent for continuous sync and large-scale transfers
  - Will be integrated when bulk operations are required

## Development Notes
- Maintain modular architecture for each phase
- Ensure robust error handling for API interactions
- Implement comprehensive logging for transfer tracking
- Design with idempotency in mind (safe to re-run operations)

---
*May the Force guide your code, Jedi Master.*
