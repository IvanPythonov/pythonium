<p align="center"> <!-- markdownlint-disable MD033 MD041 MD045 MD013-->
  <h1 align="center">pythonium</h1>
  <p align="center">
    <b>High-performance, asynchronous Minecraft server implementation (Protocol 772)</b><br>
    <i>Built with modern Python 3.14, focused on extreme throughput and low latency.</i>
  </p>
</p>

<div align=center>

![WIP](https://img.shields.io/badge/Status-Work_In_Progress-9ccbfb?style=for-the-badge&labelColor=101418)
![Python Version](https://img.shields.io/badge/python-3.14-9ccbfb?style=for-the-badge&labelColor=101418)
![GitHub last commit](https://img.shields.io/github/last-commit/IvanPythonov/pythonium?style=for-the-badge&labelColor=101418&color=9ccbfb)
![GitHub Repo stars](https://img.shields.io/github/stars/IvanPythonov/pythonium?style=for-the-badge&labelColor=101418&color=b9c8da)
![GitHub repo size](https://img.shields.io/github/repo-size/IvanPythonov/pythonium?style=for-the-badge&labelColor=101418&color=d3bfe6)

</div>

> [!Warning]
> **Pythonium** is currently in the **WIP stage**. While the networking core and dependency injection are built for high performance, the world logic and physics are still experimental. **Not for production use!**

## Quick start

```sh
# Clone the repository
git clone https://github.com/IvanPythonov/pythonium
cd pythonium

# Start with Docker
docker compose up -d
```

---

## Overview

**Pythonium** is a high-performance Minecraft server core built from the ground up. It challenges the "Python is slow" stereotype by utilizing low-level event loops, zero-copy memory views, and ultra-fast serialization

### 🚀 Key Features

- **Protocol 772 Support**: Full compatibility with Minecraft 1.21.8.
- **Extreme Serialization**: Powered by `msgspec` for near-instant binary packet processing.
- **Asynchronous Core**: Built on `asyncio` with `uvloop` (Linux) or `winloop` (Windows) for maximum throughput.
- **Type-Safe**: Leveraging Python 3.14+ features like `Generic Type Aliases` and `Annotated` types.
- **Modular Routing**: Clean, FastAPI-inspired routing system with built-in Dependency Injection.

---
