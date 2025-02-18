# kaggle

https://www.kaggle.com/datasets/adilshamim8/global-traffic-accidents-dataset

# Setup

#### Create the virtual environment (replace .venv with your preferred name)

```
python3 -**m venv .venv
```

#### **Activate the virtual environment (Windows)**

```powershell
.venv\Scripts\activate
```

#### Activate the virtual environment (macOS/Linux)

```
source .venv/bin/activate
```

#### Install the required packages	

```python
pip install -r requirements.txt
```

#### Create env

Install `python-dotenv`

`pip install python-dotenv`

Create a `.env` file

`KAGGLE_DATASET_SLUG=your_actual_dataset_slug`

---

#### Kaggle API Credentials

1. Go to your Kaggle account settings: https://www.kaggle.com/account
2. Scroll down to the "API" section and click "Create New API Token". This will download a file named `kaggle.json`.
3. Move the `kaggle.json` file to the `.kaggle` directory in your user home directory:

   - On Windows:

     ```sh

     mkdir %USERPROFILE%\.kaggle

     move C:\Path\To\Your\kaggle.json %USERPROFILE%\.kaggle\kaggle.json

     ```
   - On macOS/Linux:

     ```sh

     mkdir -p ~/.kaggle

     mv /path/to/your/kaggle.json ~/.kaggle/kaggle.json

     ```

---

# Usage

1. Ensure your virtual environment is activated.
2. Run your Python script:

   ```sh
   python main.py

   ```

---

---

---
