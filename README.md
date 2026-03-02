# GRCS Simulator

A comprehensive Golden Record Confidence Score (GRCS) Simulator with multiple calculation modules.

## Features

- 🎯 **Simulator**: Calculate GRCS scores for data matching
- 📊 **GRCS Reference Table**: View complete attribute reference
- 📖 **Technical Documentation**: Detailed methodology documentation
- ⚖️ **Weight Calculation**: ACS model calculator with L, U, S, R parameters
- 📈 **LUSR Calculation**: LUSR methodology framework

## Deployment

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add logo images to the `assets/` folder (optional):
   - `logo1.png` - First logo (e.g., DPT logo)
   - `logo2.png` - Second logo (e.g., Organization emblem)

3. Run the application:
```bash
streamlit run "import streamlit as st.py"
```

### Render Deployment

1. Push code to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Connect your repository: `https://github.com/Aniket2110m/GRCS`
4. Configuration:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run "import streamlit as st.py" --server.port=$PORT --server.address=0.0.0.0`

## Project Structure

```
.
├── import streamlit as st.py  # Main application
├── requirements.txt            # Python dependencies
├── data/                      # Reference data files
│   ├── GRCS.xlsx
│   ├── GRCS_Technical_Documentation.docx
│   ├── Weight Calculation.docx
│   └── LUSR Calculation.docx
├── assets/                    # Static assets (logos)
└── .streamlit/
    └── config.toml           # Streamlit configuration
```

## Technologies

- **Streamlit** - Web application framework
- **Pandas** - Data manipulation
- **python-docx** - Document processing
- **openpyxl** - Excel file handling

## License

MIT License
