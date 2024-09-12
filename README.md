# QuickCompress

[![GitHub release](https://img.shields.io/badge/release-latest-brightgreen)](https://github.com/EzClippy/QuickCompress/releases/latest) &nbsp; [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

![banner](./assets/banner.png)

QuickCompress ist eine benutzerfreundliche GUI-Anwendung zum Komprimieren und Ändern der Grösse von Bildern. Sie unterstützt verschiedene Bildformate und ermöglicht es den Benutzern, die gewünschte Ausgabengrösse und das gewünschte Format auszuwählen. Die Anwendung ist plattformübergreifend und intuitiv gestaltet, sodass sie für Benutzer aller Erfahrungsstufen zugänglich ist.

## Funktionen

- **Massen- und Einzelbildverarbeitung:** Komprimieren und Ändern der Grösse von Bildern in grossen Mengen oder einzeln.
- **Umfassende Formatunterstützung:** Unterstützte Eingabeformate: PNG, JPG, JPEG, BMP, GIF, WEBP, AVIF, TIFF, TIF. Unterstützte Ausgabeformate: WEBP, PNG, JPG, JPEG.
- **Benutzerfreundliche Oberfläche:** Einfache GUI mit Fortschrittsanzeige.
- **Plattformübergreifend:** Kompatibel mit Windows, macOS und Linux.

## Installation

### Voraussetzungen

- **Python 3.x** - Stellen Sie sicher, dass Python installiert ist.
- **[Pillow](https://python-pillow.org/)** - Ein Fork der Python Imaging Library.

### Einrichtung

1. **Repository klonen:**

   ```sh
   git clone https://github.com/EzClippy/QuickCompress.git
   cd QuickCompress
   ```

2. **Erstellen und Aktivieren einer virtuellen Umgebung:**

   - **Windows:**

   ```cmd
   .\activate-venv.bat
   ```

   - **Linux:**

   ```sh
   ./activate-venv.sh
   ```

3. **Abhängigkeiten installieren:**
   ```sh
   pip install -r requirements.txt
   ```

## Verwendung

1. **Die Anwendung starten:**
   ```sh
   python app.py
   ```
2. **Folgen Sie den Anweisungen in der GUI:**
   - Wählen Sie Eingabedateien oder -verzeichnis aus.
   - Wählen Sie Ausgabeformat und -grösse.
   - Klicken Sie auf „Komprimieren“, um die Verarbeitung zu starten.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE](LICENSE)-Datei für weitere Details.

## Danksagungen

- **[Pillow](https://python-pillow.org/):** Für die leistungsstarken Bildverarbeitungsfunktionen.
- **[Tkinter](https://docs.python.org/3/library/tkinter.html):** Für das GUI-Framework.
