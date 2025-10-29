"""
Django management command to compile translation files (.po to .mo)
Windows-friendly, no gettext required!
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings

try:
    import polib
    POLIB_AVAILABLE = True
except ImportError:
    POLIB_AVAILABLE = False


class Command(BaseCommand):
    help = 'Compile .po translation files to .mo format (Windows-friendly, no gettext needed)'

    def handle(self, *args, **options):
        if not POLIB_AVAILABLE:
            self.stdout.write(self.style.ERROR(
                '❌ polib is not installed. Install it with: pip install polib'
            ))
            return
        
        # Get locale directories from settings
        locale_paths = getattr(settings, 'LOCALE_PATHS', [])
        if not locale_paths:
            # Try default location
            locale_paths = [os.path.join(settings.BASE_DIR, 'locale')]
        
        compiled_count = 0
        error_count = 0
        
        for locale_dir in locale_paths:
            if not os.path.exists(locale_dir):
                self.stdout.write(self.style.WARNING(
                    f'⚠️  Locale directory not found: {locale_dir}'
                ))
                continue
            
            self.stdout.write(f'📂 Scanning: {locale_dir}')
            
            for root, dirs, files in os.walk(locale_dir):
                for file in files:
                    if file.endswith('.po'):
                        po_path = os.path.join(root, file)
                        mo_path = po_path.replace('.po', '.mo')
                        
                        try:
                            # Load .po file
                            po = polib.pofile(po_path)
                            
                            # Save as .mo file
                            po.save_as_mofile(mo_path)
                            
                            self.stdout.write(self.style.SUCCESS(
                                f'✅ Compiled: {os.path.relpath(po_path)} → {os.path.relpath(mo_path)}'
                            ))
                            compiled_count += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(
                                f'❌ Error compiling {po_path}: {e}'
                            ))
                            error_count += 1
        
        # Summary
        self.stdout.write('')
        if compiled_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'🎉 Successfully compiled {compiled_count} translation file(s)!'
            ))
            self.stdout.write(self.style.WARNING(
                '⚠️  Please restart the Django server for changes to take effect.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '⚠️  No .po files found to compile.'
            ))
        
        if error_count > 0:
            self.stdout.write(self.style.ERROR(
                f'❌ Failed to compile {error_count} file(s).'
            ))

