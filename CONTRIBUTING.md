# Contributing to SafeAgent

All contributions to SafeAgent are welcome. To ensure a smooth and effective development process for everyone, all contributors must adhere to the following rules and guidelines. This document outlines the required procedures for submitting issues and code.

## General Contribution Rules

### Rule 1: Search Before Creating
Before submitting a new bug report or feature request, you **must** search the existing [Issues](https://github.com/ViktorVeselov/SafeAgent/issues) to ensure a similar one does not already exist.

### Rule 2: Bug Reports
All bug reports **must** be submitted as a new GitHub Issue and include:
* A clear, descriptive title.
* A detailed description of the bug.
* Step-by-step instructions to reproduce the bug.

### Rule 3: Feature Requests
All feature requests **must** be submitted as a new GitHub Issue and include:
* A clear, descriptive title.
* A detailed explanation of the proposed feature and its benefits to the project.

## Code Contribution Rules

All code contributions must be submitted via a Pull Request and must follow these rules.

1.  **Work from a Fork:** All work must be done on a personal fork of the main repository. Do not commit directly to the upstream repository.

2.  **Use Feature Branches:** All changes must be made on a new branch with a descriptive name (e.g., `feat/new-caching-policy`, `fix/orchestrator-bug`). Do not commit directly to your `main` branch.

3.  **Ensure Tests Pass:** All existing tests **must** pass. If you are adding new functionality, you **must** add corresponding tests. Run `pytest` locally to validate your changes before pushing.

4.  **Adhere to Commit Message Format:** Commit messages are not arbitrary. They **must** follow the specified format to maintain a clean and readable history.

    **Required Format:**
    ```
    <type>: <subject>

    [optional body]
    ```
    * **`<type>`:** Must be one of: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
    * **`<subject>`:** Must be a concise, imperative description of the change.
    * **Example:** `git commit -m "feat: Add retry policy to ToolRegistry"`

5.  **Submit Clear Pull Requests:** Your Pull Request **must** link to the issue it resolves (if applicable) and include a clear description of the "what" and "why" of your changes.

## Code of Conduct
All contributors are required to abide by the project's Code of Conduct. (We recommend creating a `CODE_OF_CONDUCT.md` file).
