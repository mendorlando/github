# Generador de contribuciones

Este script crea un commit por día del mes elegido, con fechas de autor y
committer correspondientes a cada día. Son contribuciones generadas; no
representan trabajo realizado en esas fechas. No reescribe commits existentes.

Requiere Python 3.9+, Git y datos de zonas horarias del sistema.

Vista previa (septiembre de 2026):

```bash
python3 contribuciones.py --month 2026-09 --email 91709718+mendorlando@users.noreply.github.com
```

Para crear los commits, repite el comando con `--apply`. Para incluir solo
lunes a viernes, añade `--weekdays`. Omite fechas futuras y días ya registrados
por este script. Requiere un repositorio limpio y `git config user.name`.

Después revisa `git log` y publica con `git push origin master`.
No se publica automáticamente. Si falla un commit, revisa `git status` y
resuelve ese cambio antes de repetir el comando.

GitHub requiere un correo asociado a tu cuenta y commits en la rama
predeterminada para contabilizarlos. La gráfica puede tardar hasta 24 horas.
https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions
