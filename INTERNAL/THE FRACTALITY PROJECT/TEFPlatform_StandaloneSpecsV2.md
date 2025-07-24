# TEF Platform - Standalone Application Specification
*Collaborative Storytelling for The Extended Fractiverse*

## Executive Summary

The TEF Platform (pronounced "teff") is a standalone web application that enables collaborative storytelling within The Extended Fractiverse. Built on principles of progressive complexity, it serves three primary audiences: readers exploring the universe, writers contributing to it, and researchers diving deep into the lore. The platform will launch independently before integrating with the broader Fractality Project.

## Core Design Philosophy

**Progressive Complexity**: Users see only what they need at their level of engagement. Simple for readers, powerful for contributors, comprehensive for lore masters.

## Primary Entry Points

### Three Clear Paths
```
📖 READ STORIES - Browse and explore the narrative universe
✍️ WRITE/CONTRIBUTE - Create and collaborate on new content  
📚 WIKI/LORE - Deep dive into characters, locations, and concepts
```

## Key Features

### 1. Reading Experience

#### Story Navigation
- **Timeline View**: Visual timeline of major story arcs
- **Character Journeys**: Follow specific characters across multiple stories
- **Location Explorer**: Map-based navigation (The Ice Age Americas, etc.)
- **Traditional Browse**: Latest, popular, genre categories

#### Reader Features
- Bookmark stories and positions
- Reading progress tracking
- Spoiler-free filtering by timeline position
- Mobile-optimized reading mode

### 2. Writing & Collaboration

#### Writer Dashboard
- **My Stories**: Drafts, published works, active branches
- **Merge Requests**: Community content awaiting review
- **Writing Prompts**: Identified gaps in the lore
- **Collaborations**: Co-writing invitations and projects

#### Creation Tools
- **Resonance Editor**: Clean, distraction-free writing interface
- **Context Panel**: Shows relevant wiki entries while writing
- **Auto-Linking**: Recognizes established names and creates connections
- **Version History**: Track all changes with visual diff tools
- **Branch Management**: Create alternate timelines with clear visualization

#### Collaboration Features
- Real-time co-editing (Google Docs style)
- Inline comments and suggestions
- Writer circles for focused groups
- Consensus voting on merge requests

### 3. Wiki/Lore System

#### Comprehensive Universe Database
- **Characters**: Full profiles, relationships, appearances across stories
- **Locations**: Maps, descriptions, associated events
- **Technologies**: CSS, Phase Shifting, devices, etc.
- **Timeline**: Chronological event tracking
- **Reality Anchors**: Immutable canon events
- **Concepts**: Philosophical and scientific principles

#### Wiki Features
- Version tracking for all entries
- Discussion pages for each article
- Automatic cross-referencing
- Spoiler warnings based on story progress
- Quick search with intelligent suggestions

### 4. Community & Gamification

#### User Progression
- **Resonance Score**: Community approval rating
- **Consensus Points**: Earned through approved contributions
- **Achievements**: Meaningful milestones (not gimmicky)
- **Contributor Badges**: Archaeologist, Worldbuilder, Lorekeeper

#### Community Tools
- Following system for writers and stories
- Activity feed with customizable filters
- Events calendar for collaborative writing sessions
- Community challenges and prompts

## Technical Architecture

### Frontend
- **Framework**: React/Vue/Svelte for responsive SPA
- **Mobile First**: PWA with offline capabilities
- **Design System**: Clean, accessible, TEF-branded components

### Backend
- **API**: RESTful with GraphQL for complex queries
- **Database**: PostgreSQL for relational data, Redis for caching
- **Version Control**: Git-based system adapted for narrative
- **Search**: Elasticsearch for powerful full-text search

### Infrastructure
- **Hosting**: Scalable cloud solution (AWS/GCP/Azure)
- **CDN**: Global content delivery for fast loading
- **Authentication**: OAuth2 with social logins
- **Export API**: Designed for future Fractality Project integration

## User Interface Design

### Design Principles
- Clean, text-focused layouts
- Minimal visual noise
- Clear typography hierarchy
- Dark/light mode options
- Accessibility first (WCAG 2.1 AA compliance)

### Key UI Elements
- **Persistent Wiki Sidebar**: Collapsible for focused reading/writing
- **Breadcrumb Navigation**: Always know where you are
- **Quick Actions**: Contextual buttons that appear when needed
- **Status Indicators**: Clear branch, canon, and version information

## Content Moderation

### Automated Systems
- Continuity checking algorithms
- Duplicate detection
- Spam/inappropriate content filters

### Human Moderation
- **Editors**: Approve merge requests, maintain quality
- **Moderators**: Community management, dispute resolution
- **Admins**: Platform oversight, major decisions

## Integration Planning

### Future Fractality Project Integration
- Shared authentication system
- API endpoints for content synchronization
- Embedded reader widget for in-game lore
- Character/location data exchange

### Export Capabilities
- JSON/XML data exports
- Markdown story exports
- EPUB generation for offline reading
- API access for third-party tools

## Launch Strategy

### Phase 1: Beta (Months 1-2)
- Core reading/writing functionality
- Basic wiki system
- Essential moderation tools
- 100 beta users

### Phase 2: Public Launch (Months 3-4)
- Full feature set
- Mobile apps (iOS/Android)
- Community features
- Marketing push

### Phase 3: Growth (Months 5-6)
- Advanced collaboration tools
- API ecosystem
- Partnership integrations
- Monetization exploration

### Phase 4: TFP Integration (Aligned with game launch)
- Seamless data synchronization
- In-game content unlocks
- Cross-platform achievements
- Unified user experience

## Success Metrics

### Engagement
- Daily/monthly active users
- Stories created per month
- Average reading time
- User retention rates

### Quality
- Merge request approval rate
- Community satisfaction scores
- Continuity error reports
- Canon consistency rating

### Growth
- New user acquisition
- Content library expansion
- Community event participation
- Cross-platform conversion (TEF → TFP)

## Access Philosophy

### Forever Free
The TEF Platform will always be completely free to use. No paywalls, no premium tiers, no financial gatekeeping. This is a gift to the community and a living demonstration of collaborative creation.

### Trust-Based Progression
- **New Users**: Full reading access, basic writing in sandbox
- **Trusted Contributors**: Earned through quality contributions and community standing
- **Editors**: Demonstrated commitment to universe consistency
- **Moderators**: Proven community leadership
- **Admins**: Core team and highly trusted community members

### Sustainability Model
- Donations accepted but never required
- Potential sponsorships that align with values
- Community-driven hosting support
- Open source contributions for development

## Conclusion

The TEF Platform will serve as the living heart of The Extended Fractiverse, allowing the community to collectively shape reality through storytelling. By launching as a standalone application, we can build a passionate community of creators before the full Fractality Project launch, ensuring a rich, vibrant universe from day one.

The platform embodies the core Fractiverse principle: reality is consensus waiting to be written.

---

*Document Version 2.0 - Standalone Application Focus*  
*Prepared for TEF Platform Development Team*