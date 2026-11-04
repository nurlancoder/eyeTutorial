# Cosmic Eye Animation 👁️✨

A professional generative ASCII art animation in Python that brings a cosmic eye to life. Watch as the eye opens naturally, blinks realistically, and then the camera dives through the pupil into a mesmerizing starfield, revealing a glowing heart-shaped nebula - all rendered with text characters, no images required.

<img width="1290" height="711" alt="Cosmic Eye Animation" src="https://github.com/user-attachments/assets/f7a08b8e-c94a-46cc-8699-33f302e3e90e" />

---

## ✨ Features

### Advanced Rendering
- **Procedural ASCII Rendering**: Builds skin, iris fibers, eyebrow hairs, stars, and nebula from NumPy noise and mathematical algorithms - converts every frame into text by mapping brightness to a sophisticated dark-to-bright character ramp
- **Timeline-Driven Animation**: Smoothly eases through distinct phases - eyelid opening, natural blinking, wandering gaze, zooming into the pupil, and a nebula that morphs from a cosmic cloud into a heart shape
- **Layered Eye Model**: Combines realistic eyelids, amber iris fibers, sclera veins, catchlights, eyelid crease, and individually stamped eyelashes - with a pupil that acts as a portal to deep space

### Space Effects
- **3,200+ Twinkling Stars**: Stars fly toward the camera with individual brightness, color variations (blue-white to golden), and realistic twinkling phases
- **Shooting Stars & Comet**: Dynamic shooting stars with fading tails and a slow-moving comet with soft glow effects
- **Star Rays**: Bright stars display sparkle rays for added visual impact
- **Heart-Shaped Nebula**: A cosmic nebula that morphs from a round cloud into a glowing heart shape with realistic color gradients

### Visual Enhancements
- **Advanced Bloom Effect**: Soft glow around bright areas with multi-pass blur
- **Vignette**: Cinematic darkening toward the edges
- **Tone Mapping**: HDR-style brightness compression for realistic lighting
- **Enhanced Color Palette**: Improved color schemes with richer, more vibrant tones

### Performance & Interactivity
- **Interactive GUI**: Built with Tkinter for cross-platform compatibility
- **Smart Redrawing**: Only redraws cells that changed, automatically adapting to your computer's speed
- **Keyboard Controls**: Press `R` to restart, `Esc` to quit
- **Comprehensive Documentation**: `Glossary.txt` explains every constant, function, variable, and abbreviation used in the code

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.7 or higher
- NumPy library

### Installation

```bash
# Windows
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe eye.py
```

On macOS or Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python eye.py
```

In VS Code, open the project folder, select the project's virtual environment as the Python interpreter, and use **Run Python File**.

### Controls
- **R**: Restart animation from beginning
- **Esc**: Close the application

---

## 🎨 Technical Highlights

### Code Quality
- **Professional Variable Naming**: All variables and functions use descriptive, self-documenting names
- **Comprehensive Documentation**: Docstrings for all major functions
- **Modular Design**: Well-organized code structure with clear separation of concerns
- **Performance Optimized**: Smart cell updating and caching for smooth 30 FPS animation

### Rendering Pipeline
1. **Texture Generation**: Fractal noise textures for skin, iris, veins, and nebula
2. **Geometry Setup**: Coordinate grids and spatial transformations
3. **Eye Rendering**: Multi-layer composition of eye components
4. **Space Rendering**: Star field, shooting stars, and nebula
5. **Post-Processing**: Bloom, tone mapping, and character mapping
6. **Display**: Smart redrawing with performance budgeting

### Key Functions
- `render_frame()`: Main rendering pipeline for each frame
- `eye_scene_renderer()`: Complete eye composition
- `heart_nebula_renderer()`: Heart-shaped nebula with morphing
- `apply_bloom()`: Multi-pass glow effect
- `render_stars()`: Twinkling star field with rays
- `render_eyelashes()`: Individual eyelash rendering

---

## 📁 Project Structure

```
eyeTutorial-main/
├── eye.py              # Main animation script (800 lines)
├── README.md           # This file
├── Glossary.txt        # Comprehensive code documentation
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes local environments and generated files
└── .gitattributes      # Git configuration
```

---

## 🎯 Configuration

Key configuration constants (at the top of `eye.py`):

```python
FONT_SIZE = 8                    # Character size
FRAME_RATE = 30                 # Target FPS
SUPER_SAMPLE = 2                 # Anti-aliasing quality
MAX_ROW_COUNT = 30               # Maximum rows to display

# Timeline (seconds)
TIME_EYE_OPEN_START = 0.9        # When eye starts opening
TIME_BLINK = 4.0                 # When blink occurs
TIME_ZOOM_START = 5.4            # When zoom to space begins
TIME_HEART_MORPH_START = 8.9      # When nebula starts becoming heart

# Visual settings
EYE_HALF_WIDTH = 0.78            # Eye opening width
IRIS_RADIUS = 0.27               # Iris size
STAR_COUNT = 3200                # Number of stars
```

---

## 🔬 How It Works

### ASCII Art Generation
1. The scene is rendered at high resolution using NumPy
2. Colors are computed for each pixel using procedural algorithms
3. The image is downsampled to character cell size
4. Brightness determines which character from the ramp to use
5. Characters are colored and displayed in Tkinter canvas

### Procedural Textures
- **Skin**: Multi-octave fractal noise
- **Iris**: 1D angular noise mapped radially
- **Veins**: Ridged noise (abs of noise)
- **Nebula**: Fractal noise with heart morphing

### Animation Timeline
```
0.0s - 0.9s:   Initialization
0.9s - 3.3s:   Eye opens smoothly
4.0s:          Natural blink
5.4s - 33.4s:  Zoom into pupil
6.9s+:         Space scene visible
8.9s+:         Heart nebula appears
```

---

## 📊 Performance

- **Target FPS**: 30 frames per second
- **Adaptive Budget**: Automatically adjusts cells per frame based on performance
- **Smart Caching**: Reuses color strings and minimizes canvas updates
- **SuperSampling**: 2x2 sub-pixels per cell for anti-aliasing

---

## 🎓 Learning Resources

The included `Glossary.txt` file provides:
- Explanation of every constant
- Description of all functions
- Variable name definitions
- Technical term glossary
- Code structure overview

Read it alongside the code to understand every aspect of the implementation.

---

## 🌟 Customization

### Change Colors
Modify color arrays in these functions:
- `eye_scene_renderer()`: Eye colors (iris, sclera, skin)
- `heart_nebula_renderer()`: Nebula colors
- `render_stars()`: Star color palette

### Adjust Timing
Modify timeline constants at the top of the file:
- `TIME_EYE_OPEN_START`: When eye opens
- `TIME_BLINK`: When blink occurs
- `TIME_ZOOM_START`: When zoom begins
- `TIME_HEART_MORPH_START`: When heart appears

### Change Character Ramp
Modify `BRIGHTNESS_RAMP` to use different ASCII characters:
```python
BRIGHTNESS_RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
```

---

## 🤝 Contributing

This is a demonstration project showcasing procedural ASCII art and real-time rendering techniques. Feel free to:
- Experiment with color schemes
- Modify animation timing
- Add new visual effects
- Optimize performance further

---

## 📜 License

This project is provided as-is for educational and demonstration purposes.

---

## 👤 Author

**Powered by Nurlan Mammadli**

🌐 GitHub: [https://github.com/nurlancoder](https://github.com/nurlancoder)

---

## 🙏 Acknowledgments

This project demonstrates advanced Python graphics programming using:
- **NumPy**: High-performance array operations
- **Tkinter**: Built-in GUI framework
- **Procedural Generation**: No external assets required

---

## 🎬 Future Enhancements

Potential improvements:
- Add configuration file support
- Implement preset color themes
- Add pause/resume functionality
- Export frames to video
- Add sound effects
- Multiple eye variations
- Customizable character sets

---

## 📞 Support

For questions or issues, please visit:
- GitHub: [https://github.com/nurlancoder](https://github.com/nurlancoder)

---

**Enjoy the cosmic journey!** 🚀✨
