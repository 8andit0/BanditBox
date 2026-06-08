---
title: sudo misconfiguration
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# sudo misconfiguration

## Descripcion

Una mala configuracion de sudo permite ejecutar binarios o scripts con privilegios excesivos. Reglas NOPASSWD, variables preservadas o comodines pueden romper el limite entre usuario y root.

## Senales de deteccion

- sudo -l con NOPASSWD
- binarios interactivos permitidos
- scripts root editables
- env_keep peligroso
- wildcards en sudoers

## Mitigacion

Limitar comandos con rutas absolutas, evitar comodines, no preservar variables peligrosas, auditar scripts permitidos y aplicar minimo privilegio.

## Guias externas

- [https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html](https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html)

## Maquinas relacionadas

- [Candy](../machines/dockerlabs/facil/candy.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)
