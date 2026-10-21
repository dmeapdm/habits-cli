# spec-generator

Skill que convierte una idea vaga en una especificación acordada (`spec.md`) y
que sabe revisar una spec existente. Procede del curso de Spec-Driven
Development de Brais Moure (`mouredev/hello-sdd`).

## Contenido

| Fichero | Qué es |
|---|---|
| `SKILL.md` | Instrucciones de la skill: entrevista de requisitos, redacción en notación EARS y modo revisión. **Única fuente de verdad.** |
| `spec-template.md` | La plantilla que la skill usa para redactar la spec. |

## Dónde está instalada

| Ámbito | Ruta | Cuándo se aplica |
|---|---|---|
| Proyecto (canónica) | `.claude/skills/spec-generator/` | Se versiona con el repo y es la copia de referencia. |
| Proyecto (opencode) | `.opencode/skill/spec-generator` → symlink a la canónica | opencode la carga en este proyecto. |
| Global | `~/.config/opencode/skill/spec-generator/` | En cualquier otro proyecto. |

## Activación

- **Automática**: se ofrece al modelo cuando pides crear, redactar o revisar
  una especificación.
- **Manual**: escribe `/spec-generator` o invócala por su nombre.

## Mantenimiento

`SKILL.md` es la única fuente de verdad. La copia global y el symlink del
proyecto apuntan a contenidos idénticos: si editas una, sincroniza las otras.

En Windows, donde los symlinks suelen fallar por falta de permisos, copia la
carpeta en vez de enlazarla:

```bash
mkdir -p .opencode/skill && cp -R .claude/skills/spec-generator .opencode/skill/
```
