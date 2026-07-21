<!-- cspell:ignore handicaps -->

# Apple Container Guide

This document gathers the `ansible-navigator`-specific behavior, requirements,
trade-offs, and usage notes for using
[apple/container](https://github.com/apple/container) as the execution
environment container engine.

## What this guide is for

Use this guide when:

- `--container-engine container` or
  `execution-environment.container-engine: container` is selected
- execution-environment behavior differs from Docker or Podman
- you need Apple Container-specific setup, troubleshooting, or operational notes

## Requirements

Using Apple Container with `ansible-navigator` currently assumes:

- macOS
- Apple Container installed and working
- the `container` CLI available on `PATH`
- internet access for pulling execution-environment images
- pre-existing registry authentication for private images via
  `container registry login <registry>`

## Installation

Basic installation flow on macOS:

1.  Install the Apple Container CLI.
2.  Ensure `container --version` works from your shell.
3.  Install `ansible-navigator`.
4.  Run with `--ce container` when using execution environments.

Example:

```bash
ansible-navigator run site.yml --ee true --ce container --mode stdout
```

## Runtime behavior

When Apple Container is selected, `ansible-navigator` now uses Apple-style image
commands:

- `container image pull`
- `container image inspect`
- `container image list`

For execution-environment runs, `ansible-navigator` passes `container` through
to `ansible-runner`, which launches the EE using `container run`.

## Passing Apple-specific engine options

`ansible-navigator` does not hide Apple Container runtime flags. When you need
runtime-specific behavior, pass those options through the normal
execution-environment container-options setting.

### CLI examples

Use repeated `--co` values to pass Apple Container flags.

Forward the host SSH agent using Apple Container's native SSH support:

```bash
ansible-navigator run site.yml --ee true --ce container --co=--ssh
```

Enable nested virtualization:

```bash
ansible-navigator run site.yml --ee true --ce container --co=--virtualization
```

Enable Rosetta in the container:

```bash
ansible-navigator run site.yml --ee true --ce container --co=--rosetta
```

You can combine them:

```bash
ansible-navigator run site.yml --ee true --ce container --co=--ssh --co=--rosetta
```

### Settings file example

Use `execution-environment.container-options` when you want these flags to be
persistent:

```yaml
ansible-navigator:
  execution-environment:
    enabled: true
    container-engine: container
    container-options:
      - "--ssh"
      - "--rosetta"
```

### Notes on important flags

`--ssh` Usually the most useful Apple-specific option. Prefer this when your
execution-environment workflow needs access to private Git repositories or other
SSH-agent-backed credentials. It is generally cleaner than trying to hand-build
equivalent socket mounts.

`--virtualization` Exposes virtualization capabilities to the container. Use
this only when the workload explicitly requires nested virtualization and the
host platform supports it.

`--rosetta` Enables Rosetta in the container. This is mainly useful for
compatibility scenarios where the container workload needs x86_64 userland
support on Apple Silicon. It should not be treated as a default setting.

## Authentication model

Apple Container uses its own registry login state.

That means:

- private-registry access should be prepared with
  `container registry login <registry>`
- `ansible-navigator` does not log in or log out on the user's behalf
- if a private image pull fails, the recommended recovery is to authenticate
  first and retry

## Advantages

Using Apple Container has some practical strengths on macOS:

- native Apple tooling for execution environments
- no requirement to depend on Docker Desktop or Podman for the validated
  Apple-specific path
- Apple-native image lifecycle commands
- working end-to-end execution-environment run and cancel behavior in the
  validated prototype and parity paths

## Handicaps and trade-offs

Apple Container support is functional, but it is not the same operational model
as Docker or Podman.

Important trade-offs:

- registry authentication is based on prior login state, not runner-managed
  auth-file injection
- some Docker/Podman-specific flags and mount-label assumptions do not apply
- container-runtime-specific output shapes required dedicated parsing in a few
  places
- auto-detection order may still prefer Podman or Docker before Apple Container
  when `container-engine: auto` is used

## FAQ

### How do I authenticate to a private registry?

Run:

```bash
container registry login <registry>
```

before invoking `ansible-navigator` against a private execution-environment
image.

### Why doesn’t `ansible-navigator` log me in automatically?

Because Apple Container login is persistent host state. The chosen design keeps
that authentication step explicit instead of hiding host-state mutation inside
runner or navigator.

### What should I do if an Apple Container image pull fails?

First confirm:

- the image name is correct
- the registry is reachable
- you have already authenticated with `container registry login <registry>` if
  the image is private

Then retry the `ansible-navigator` command.

### Does `auto` always choose Apple Container?

No. `auto` still preserves its configured preference order. If another supported
engine is preferred and available, it may be selected first.

### Are Docker and Podman behaviors changed by this guide?

No. This guide exists specifically because Apple Container has runtime-specific
differences that should be documented without changing the meaning of the
existing Docker/Podman paths.
