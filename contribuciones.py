#!/usr/bin/env python3
"""Genera commits fechados para un mes. Sin --apply solo muestra el plan."""
import argparse
import calendar
from datetime import date, datetime
import os
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo


def git(*args, env=None):
    return subprocess.check_output(['git', *args], text=True, env=env).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--month', required=True, help='Mes YYYY-MM, por ejemplo 2026-09')
    parser.add_argument('--email', required=True, help='Correo asociado a tu cuenta de GitHub')
    parser.add_argument('--weekdays', action='store_true', help='Solo lunes a viernes')
    parser.add_argument('--apply', action='store_true', help='Crear los commits localmente')
    args = parser.parse_args()
    try:
        start = date.fromisoformat(args.month + '-01')
    except ValueError:
        parser.error('Usa un mes válido con formato YYYY-MM.')
    if not args.email.strip() or '\n' in args.email:
        parser.error('Indica un correo válido.')
    root = Path(git('rev-parse', '--show-toplevel'))
    os.chdir(root)
    target = root / 'contribuciones-generadas.txt'
    if target.is_symlink():
        parser.error('El archivo de registro no puede ser un enlace simbólico.')
    existing = set(target.read_text().splitlines()) if target.exists() else set()
    today = datetime.now(ZoneInfo('America/Mexico_City')).date()
    days = [date(start.year, start.month, d)
            for d in range(1, calendar.monthrange(start.year, start.month)[1] + 1)]
    days = [d for d in days if d <= today and (not args.weekdays or d.weekday() < 5)
            and f'Contribución generada: {d}' not in existing]
    print(f'Rama: {git("branch", "--show-current")} | Correo: {args.email}')
    print(f'{len(days)} commits pendientes: ' + ', '.join(map(str, days)))
    if not args.apply:
        print('Vista previa. Añade --apply para crearlos; no se hace push automáticamente.')
        return
    if git('status', '--porcelain'):
        parser.error('Guarda o confirma tus cambios primero: el repositorio debe estar limpio.')
    if not git('branch', '--show-current'):
        parser.error('Debes estar en una rama, no en detached HEAD.')
    if not git('config', 'user.name'):
        parser.error('Configura git config user.name antes de continuar.')
    for day in days:
        stamp = datetime(day.year, day.month, day.day, 12,
                         tzinfo=ZoneInfo('America/Mexico_City')).isoformat()
        env = dict(os.environ, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp,
                   GIT_AUTHOR_EMAIL=args.email, GIT_COMMITTER_EMAIL=args.email)
        with target.open('a') as output:
            output.write(f'Contribución generada: {day}\n')
        git('add', '--', target.name)
        git('-c', 'commit.gpgsign=false', 'commit', '-m',
            f'Contribución generada para {day}', env=env)
    print('Terminado. Revisa git log antes de publicar con git push.')


if __name__ == '__main__':
    main()
