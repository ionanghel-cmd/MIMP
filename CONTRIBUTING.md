# Contributing to MotoERP

Thank you for your interest in contributing! Here's how to get involved.

## 📋 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn
- Report issues professionally

## 🚀 Getting Started

### 1. Fork and Clone
```bash
git clone <your-fork>
cd moto-erp
```

### 2. Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
# Edit with your Supabase credentials
```

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## 💻 Development Workflow

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

### Before Committing
```bash
# Format code
python -m py_compile app/*.py

# Test locally
streamlit run app/app.py

# Check git status
git status
```

### Commit Messages
```
Format: [Type] Subject

Types: feat, fix, docs, style, refactor, perf, test, chore

Examples:
[feat] Add email notifications
[fix] Fix profit calculation bug
[docs] Update setup guide
[refactor] Improve database queries
```

### Pull Request Process
1. Create descriptive PR title
2. Explain what changed and why
3. Link related issues
4. Wait for review
5. Make requested changes
6. Request re-review

## 📝 Feature Development

### Adding a New Feature

1. **Plan in ROADMAP.md**
   - What phase?
   - What does it do?
   - What's the scope?

2. **Create Issue**
   - Describe feature
   - Add acceptance criteria
   - Link to phase/roadmap

3. **Implement**
   - Create feature branch
   - Write code
   - Update docs
   - Test thoroughly

4. **Test**
   - Manual testing
   - Edge cases
   - Error handling
   - Performance

5. **Document**
   - Update README.md if UI changes
   - Update ARCHITECTURE.md if system changes
   - Add code comments
   - Update docstrings

6. **Submit PR**
   - Include tests
   - Link issue
   - Describe changes

## 🐛 Bug Fixes

1. **Report Issue**
   - Describe bug clearly
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshot/error if possible

2. **Create Fix Branch**
   ```bash
   git checkout -b fix/bug-name
   ```

3. **Implement Fix**
   - Fix the root cause
   - Don't add features
   - Keep changes minimal

4. **Test Fix**
   - Verify bug is fixed
   - Verify no new bugs
   - Test edge cases

5. **Document**
   - Update IMPLEMENTATION_CHECKLIST.md if relevant
   - Add comments explaining fix

## 📚 Documentation Contributions

### Update Documentation
```bash
git checkout -b docs/update-name
# Edit .md files
git add docs/
git commit -m "[docs] Description"
```

### Documentation Guidelines
- Use clear, simple language
- Include examples
- Use markdown formatting
- Link to related docs
- Keep up to date

## 🧪 Testing

### Manual Testing Checklist
- [ ] Feature works as expected
- [ ] No errors in console
- [ ] No database errors
- [ ] Performance acceptable
- [ ] Works on different browsers
- [ ] Mobile responsive (if applicable)

### Test Coverage
Future: Implement automated tests
- Unit tests (app/tests/test_*.py)
- Integration tests
- E2E tests

## 🔍 Code Review Guidelines

### As a Reviewer
- Be constructive and kind
- Ask questions instead of demanding
- Approve when satisfied
- Suggest improvements

### As an Author
- Respond to feedback promptly
- Ask for clarification if needed
- Make requested changes
- Thank reviewers

## 📚 Architecture Decisions

### Before Making Major Changes
1. Discuss in issue/PR
2. Consider alternatives
3. Document decision
4. Get team consensus

### Document Changes In
- ARCHITECTURE.md
- Code comments
- Commit message

## 🚀 Deployment

### Staging
```bash
git push origin feature/your-feature
# Deploy to staging environment
```

### Production
```bash
git checkout main
git merge feature/your-feature
git tag -a v0.2.0
git push origin main --tags
# Deploy to production
```

## 📊 Monitoring After Deployment

- Check error logs
- Monitor performance
- Get user feedback
- Fix critical issues immediately

## 🎯 Priority Areas for Contribution

### High Priority
- Bug fixes
- Performance improvements
- Documentation
- Testing infrastructure

### Medium Priority
- Phase 2 features (authentication, API)
- UI improvements
- Database optimization

### Future
- Phase 3 features (analytics, integrations)
- Phase 4 features (SaaS)

## 📖 Resources

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [ROADMAP.md](ROADMAP.md) - Development plan
- [Streamlit Docs](https://streamlit.io/docs)
- [Supabase Docs](https://supabase.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs)

## ❓ Questions?

- Create an issue
- Start a discussion
- Check existing issues
- Review documentation

## 🙏 Thank You!

Contributing makes MotoERP better for everyone. We appreciate your help!

---

**Last Updated:** July 2026
**Version:** 0.1.0
