# Contributing to Qiskit Studio

Thank you for your interest in contributing to Qiskit Studio! This guide will help you get started.

## Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (for Python dependencies)
- [Ollama](https://ollama.com) (for local LLM support)
- Git

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/qiskit-studio
   cd qiskit-studio
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment:**
   ```bash
   cp .env.local.template .env.local
   # Edit .env.local with your configuration
   ```

4. **Set up API agents:**
   ```bash
   # Each agent has its own .env.template in its directory
   cd api/chat-agent && cp .env.template .env && cd ../..
   cd api/codegen-agent && cp .env.template .env && cd ../..
   cd api/coderun-agent && cp .env.template .env && cd ../..
   ```

5. **Start the development server:**
   ```bash
   npm run dev
   ```

6. **Start API agents** (in separate terminals):
   ```bash
   # Chat agent
   cd api/chat-agent/
   uv run maestro serve agents.yaml workflow.yaml
   
   # Code generation agent
   cd api/codegen-agent/
   uv run maestro serve agents.yaml workflow.yaml --port 8001
   
   # Code run agent
   cd api/coderun-agent/
   uv run python agent.py --port 8002
   ```

7. **Set up vector database** (for chat agent):
   ```bash
   git clone https://github.com/AI4quantum/maestro-knowledge.git
   cd maestro-knowledge
   CUSTOM_EMBEDDING_URL=http://127.0.0.1:11434/v1 \
   CUSTOM_EMBEDDING_MODEL=nomic-embed-text \
   CUSTOM_EMBEDDING_VECTORSIZE=768 \
   CUSTOM_EMBEDDING_API_KEY=dummy \
   uv run ./start.sh
   
   # Populate the database
   cd ../qiskit-studio/api/chat-agent/
   uv run python scripts/add-rag-docs-remote-embed.py
   ```

8. **Access the application:**
   Open [http://localhost:3000](http://localhost:3000)

For detailed API setup instructions, see [api/README.md](api/README.md).

## How to Contribute

### Reporting Issues

Before creating an issue, please check [existing issues](https://github.com/AI4quantum/qiskit-studio/issues).

When reporting bugs, include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (for UI issues)
- Environment details (OS, Node version, etc.)

### Suggesting Features

- Check [GitHub Discussions](https://github.com/AI4quantum/qiskit-studio/discussions) first
- Describe the feature and its benefits
- Provide use cases
- Suggest implementation approach if possible

### Contributing Code

1. **Find or create an issue** to work on
2. **Comment on the issue** to let others know you're working on it
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Commit your changes:**
   ```bash
   git commit -m "feat: add new feature"
   ```
7. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request** on GitHub

## Development Guidelines

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Maintenance tasks

**Example:**
```
feat(nodes): add quantum chemistry node

Implements a new node for quantum chemistry calculations
using PySCF integration.

Closes #123
```

### Coding Standards

#### TypeScript/JavaScript
- Use TypeScript for all new code
- Follow existing code style
- Use meaningful variable and function names
- Add comments for complex logic
- Run `npm run lint` before committing

#### Python
- Follow PEP 8 style guide
- Use type hints
- Add docstrings for public functions and classes
- Keep functions focused and small

### Secret Detection

This project uses [detect-secrets](https://github.com/IBM/detect-secrets) to prevent committing secrets.

**Setup:**
```bash
pip install detect-secrets
pip install pre-commit
pre-commit install
```

**Usage:**
```bash
# Scan for secrets
detect-secrets scan

# Update baseline
detect-secrets scan --update .secrets.baseline

# Audit detected secrets
detect-secrets audit .secrets.baseline
```

**Best Practices:**
- Never commit real secrets
- Use environment variables
- Update baseline for false positives
- Add `# pragma: allowlist secret` for unavoidable cases

## Documentation

- Update relevant docs in `docs/` directory
- Keep README.md current
- Add examples for new features
- Update API documentation in `api/README.md`
- Include inline code comments

## Pull Request Process

### Before Submitting

1. **Update your branch** with latest changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run linting:**
   ```bash
   npm run lint
   ```

3. **Test your changes** thoroughly

4. **Update documentation** as needed

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] No secrets in code (detect-secrets passed)
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] PR description is clear and complete

### PR Description

Include:
- Clear description of changes
- Reference to related issues
- Screenshots/GIFs for UI changes
- Breaking changes (if any)

## Project Structure

```
qiskit-studio/
├── app/                 # Next.js app directory
├── components/          # React components
│   ├── nodes/          # Quantum computing nodes
│   └── ui/             # UI components
├── lib/                # Utility functions
├── api/                # Backend API agents
│   ├── chat-agent/     # Chat/RAG agent
│   ├── codegen-agent/  # Code generation agent
│   └── coderun-agent/  # Code execution agent
├── docs/                # Documentation
└── public/             # Static assets
```

## Available Scripts

```bash
npm run dev         # Start development server
npm run build       # Build for production
npm run start       # Start production server
npm run lint        # Run ESLint
```

## Community

- **[GitHub Discussions](https://github.com/AI4quantum/qiskit-studio/discussions)** - Ask questions and discuss ideas
- **[GitHub Issues](https://github.com/AI4quantum/qiskit-studio/issues)** - Report bugs and request features

## Additional Resources

- [Usage Guide](docs/usage.md) - How to use Qiskit Studio
- [Architecture](docs/architecture.md) - System architecture overview
- [Node Documentation](docs/nodes.md) - Available quantum computing nodes
- [API Documentation](api/README.md) - Backend API setup

## License

By contributing to Qiskit Studio, you agree that your contributions will be licensed under the Apache License 2.0.

## Questions?

If you have questions about contributing:
- Open a [Discussion](https://github.com/AI4quantum/qiskit-studio/discussions)
- Comment on relevant issues
- Check existing documentation

Thank you for contributing to Qiskit Studio! 🎉