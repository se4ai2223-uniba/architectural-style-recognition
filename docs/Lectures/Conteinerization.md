# Conteinarization 📦

## Software Portability 

Portabiliy: Where, the software, can run.

- Heavy Solution: VM (Snapshot of the computer)
- Light Solution: Container

## Differences

- Virtual Machine need to communicate between two operating system managing App, Bins/Lib, Guest OS (for each app) (slower)

- With containers the operating system is just one and it handle, for each app, just the app and bins/libs. (faster)

the only case in which VM is better than container, is for test-security reasons.

## Some technologies that support Conteinerization

- Docker 🐋
- Kubernetes 🟥 (orchestrate services: which container start first, which later, handle errors in containers)

//prossima lezione: Giovedi
