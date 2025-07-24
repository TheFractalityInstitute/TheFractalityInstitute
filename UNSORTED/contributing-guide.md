# Contributing to The Fractality Institute 🤝

First off, thank you for considering contributing to The Fractality Institute! We're building something unprecedented: a framework that bridges mathematics, consciousness, and reality itself. Every contribution, whether it's uploading EEG data or refining our philosophical frameworks, advances human understanding.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Canon-Specific Guidelines](#canon-specific-guidelines)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Recognition](#recognition)

---

## Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Please report unacceptable behavior to ethics@fractality.institute.

---

## How Can I Contribute?

### 🧪 As a Citizen Scientist
- **Upload EEG Data**: Participate in the Riemann Resonance Project
- **Test Protocols**: Try wellness protocols and report results
- **Validate Findings**: Attempt to replicate published results
- **Share Experiences**: Document subjective experiences rigorously

### 💻 As a Developer
- **Fix Bugs**: Check our [issue tracker](https://github.com/fractality-institute/fractality-institute/issues)
- **Add Features**: Implement items from our roadmap
- **Improve Documentation**: Help others understand the code
- **Create Tools**: Build analysis or visualization tools

### 🔬 As a Researcher
- **Design Studies**: Submit pre-registered protocols
- **Analyze Data**: Apply statistical methods to our datasets
- **Peer Review**: Review others' pre-registrations and papers
- **Synthesize Knowledge**: Write review articles or meta-analyses

### 🎨 As a Creative
- **Write Fiction**: Expand the Fractiverse mythology
- **Create Visuals**: Design infographics or data visualizations
- **Produce Media**: Make videos explaining concepts
- **Artistic Expression**: Interpret ideas through your medium

---

## Canon-Specific Guidelines

### 📊 Canon I: Empirical Contributions

**Requirements:**
- All claims must be falsifiable
- Data must include methodology
- Statistical analysis required
- Negative results welcomed

**Process:**
1. Pre-register your study using our [template](contributing/pre-registration/empirical-template.md)
2. Collect data following ethical guidelines
3. Analyze using our standard pipeline
4. Submit with full transparency

**Example PR title**: `[Canon I] Add EEG coherence analysis for meditation study`

### 🔧 Canon II: Engineering Contributions

**Requirements:**
- Code must be tested
- Documentation required
- Consider performance
- Ensure compatibility

**Process:**
1. Discuss design in issue first
2. Write tests before code
3. Follow style guidelines
4. Update documentation

**Example PR title**: `[Canon II] Implement wavelet analysis for Riemann detection`

### 💭 Canon III: Speculative Contributions

**Requirements:**
- Internal logical consistency
- Clear about assumptions
- Connect to other frameworks
- Acknowledge limitations

**Process:**
1. Ground speculation appropriately
2. Use precise language
3. Cross-reference other work
4. Suggest empirical tests

**Example PR title**: `[Canon III] Propose quantum coherence model for memory`

### 📚 Canon IV: Narrative Contributions

**Requirements:**
- Thematic consistency
- Respect established lore
- Creative expansion welcomed
- Various media accepted

**Process:**
1. Read existing narratives
2. Propose your addition
3. Get community feedback
4. Submit polished work

**Example PR title**: `[Canon IV] Add Chapter 3 to Crystallized Beings saga`

---

## Development Process

### 1. Before You Start

**Check existing work:**
```bash
# Search issues for similar ideas
https://github.com/fractality-institute/fractality-institute/issues

# Check project boards
https://github.com/fractality-institute/fractality-institute/projects

# Join Discord discussion
https://discord.gg/YOUR_INVITE
```

### 2. Setting Up Your Environment

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/YOUR_USERNAME/fractality-institute.git

# Add upstream remote
git remote add upstream https://github.com/fractality-institute/fractality-institute.git

# Create a new branch
git checkout -b feature/your-feature-name
```

### 3. Making Changes

**For Code:**
```python
# Run tests before committing
pytest tests/

# Check code style
flake8 your_file.py

# Format code
black your_file.py
```

**For Documentation:**
- Use clear, concise language
- Include examples
- Add cross-references
- Update table of contents

### 4. Testing

**Automated Tests:**
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_riemann_analysis.py

# Check coverage
pytest --cov=fractality
```

**Manual Testing:**
- Test with real data
- Verify documentation accuracy
- Check cross-platform compatibility

---

## Style Guidelines

### Python Code Style
```python
"""
Module docstring explaining purpose.

Follows Google Python Style Guide with modifications.
"""

def detect_riemann_signature(data: np.ndarray, 
                           sampling_rate: float,
                           scaling_range: Tuple[float, float] = (-2, 2)) -> Dict:
    """
    Detect Riemann zero signatures in time series data.
    
    Args:
        data: Time series data as numpy array
        sampling_rate: Sampling frequency in Hz
        scaling_range: Range for scaling parameter search
        
    Returns:
        Dictionary containing detection results and statistics
        
    Example:
        >>> results = detect_riemann_signature(eeg_data, 256.0)
        >>> print(f"Correlation: {results['correlation']}")
    """
    # Implementation here
    pass
```

### Documentation Style
```markdown
# Clear Heading

Brief introduction paragraph explaining the concept.

## Subsection

- Use bullet points for lists
- Keep paragraphs short
- Include code examples
- Add relevant links

**Important**: Highlight key information

> Quote sources appropriately
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(riemann): add wavelet analysis for better frequency resolution

The new wavelet analysis provides time-frequency localization that
improves detection of non-stationary Riemann signatures in EEG data.

Closes #123
```

---

## Pull Request Process

### 1. Pre-submission Checklist

- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Style guidelines followed
- [ ] Commit messages clear
- [ ] Branch up to date with main

### 2. Creating the PR

**Title Format**: `[Canon X] Brief description`

**PR Template:**
```markdown
## Description
Brief description of changes and motivation

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] My code follows style guidelines
- [ ] I have performed self-review
- [ ] I have commented complex code
- [ ] I have updated documentation
- [ ] My changes generate no warnings
```

### 3. Review Process

**What to expect:**
1. Automated checks run
2. Peer review within 48h
3. Feedback and discussion
4. Approval from maintainer
5. Merge to main branch

**Responding to feedback:**
- Address all comments
- Ask for clarification if needed
- Update PR based on suggestions
- Re-request review when ready

---

## Recognition

### Contributor Levels

**🌱 Seedling** (First PR merged)
- Added to contributors list
- Discord role granted

**🌿 Growing** (5 PRs merged)
- Invitation to maintainers meeting
- Early access to new features

**🌳 Established** (10 PRs merged)
- Voting rights on proposals
- Can approve simple PRs

**🌲 Ancient** (25+ PRs merged)
- Core team consideration
- Shape project direction

### Special Recognition

**🔬 Data Champion**: Significant data contributions  
**🏗️ Architect**: Major feature implementation  
**📚 Scholar**: Exceptional documentation  
**🎨 Artist**: Outstanding creative work  
**🤝 Collaborator**: Excellent teamwork  
**💡 Innovator**: Breakthrough ideas

---

## Questions?

- 💬 Ask on Discord `#contributing` channel
- 📧 Email: contribute@fractality.institute
- 🐦 Twitter: @fractality_inst
- 📖 Read our [FAQ](docs/FAQ.md)

---

<div align="center">

**Every contribution advances human understanding of consciousness.**

Thank you for being part of this journey! 🙏

</div>