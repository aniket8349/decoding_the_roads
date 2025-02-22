# kaggle

https://www.kaggle.com/datasets/adilshamim8/global-traffic-accidents-dataset

# Setup

### Create the virtual environment

Using `venv` (recommended for Python 3):(replace .venv with your preferred name)

```
python3 -m venv .venv
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

### Create env

#### Install `python-dotenv`

`pip install python-dotenv`

#### Create a `.env` file

`KAGGLE_DATASET_SLUG=your_actual_dataset_slug`

---

### Mysql setup

#### Install MySQL Server

Follow the instructions to install MySQL Server on your machine:

- [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)

#### Create a MySQL Database

1. Open MySQL command line or MySQL Workbench.
2. Create a new database:

   ```sql

   CREATE DATABASE your_database_name;

   ```

#### Configure Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```env
MYSQL_HOST=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DATABASE=
```

---

### Kaggle API Credentials

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
   python -m decoding_the_roads.main
   ```

---

---

---
