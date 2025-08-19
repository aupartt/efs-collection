# Collectes EFS

A comprehensive data collection and analysis system for the French Blood Service (EFS) API. This project retrieves, processes, and stores EFS collection data to provide insights into blood donation schedules and locations across Brittany.

## 📊 What This Project Does

The system automatically:
- 🗺️ **Discovers** blood donation locations across Brittany
- 📅 **Retrieves** collection schedules and availability
- 🕷️ **Crawls** detailed appointment data from EFS websites  
- 💾 **Stores** everything in SQL database
- ⏰ **Schedules** regular updates to keep data fresh

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd collectes-efs
   ```

2. **Setup `.env`**
   
   ```bash
   cp .env.example .env

   # ... change variables
   ```

3. **Build all services**

   ```bash
   docker compose build
   ```

4. **Start the infrastructure**

   ```bash
   docker compose up -d
   ```

5. **Init database**

   This service should have started with the previous step
   ```bash
   docker compose run --rm alembic
   ```
   
6. **First run**

   Don't forget to make a first run to init **groups** and **locations**
   ```bash
   docker compose run --rm cli --groups --locations
   ```

## 📋 CLI Usage
### Parameters
| Long | Short | Type | Default | Description |
|-----------|------|-----------|---------|---|
| **--file** | **-f** | str | `None` | Path to the file |
| **--format** | **-F** | `JSON`, `JSONL` | `JSONL` | Update appointment availability |
| **--groups** | **-g** | bool | `False` | Update groups database |
| **--locations** | **-l** | bool | `False` | Update location database |
| **--collections** | **-c** | bool | `False` | Refresh collection events |
| **--schedules** | **-s** | bool | `False` | Update appointment availability |

### Start collecte

```bash
# Start a single collect
docker compose run --rm cli --groups

# Start multiple collecte
docker compose run --rm cli --collections --schedules
```

### Insert data from file
Make sure to put you file into the `./data/` folder

```bash
# The ./data folder of this project is mounted at ../data/ 
docker compose run --rm cli --collections --file ../data/collections.json
```


## ⏰ Automated Scheduling (optional)

You can use `run-collectes.sh` and `crontab-collectes` to schedule automated data collection.

### Default scheduled Tasks
| Task | Frequency | Purpose |
|------|-----------|---------|
| `get-groups` | Weekly (Sun 3 AM) | Update groups database |
| `get-locations` | Weekly (Sun 3:30 AM) | Update location database |
| `get-collections` | Daily (11 AM) | Refresh collection events |
| `get-schedules` | Twice daily (11:30 AM) | Update appointment availability |

**Setup automated scheduling**
```bash
   # 1. Copy the script
   sudo cp run-collectes.sh /usr/local/bin/
   sudo chmod +x /usr/local/bin/run-collectes.sh

   # 2. Update the path in the script
   sudo nano /usr/local/bin/run-collectes.sh
   # Change PROJECT_DIR="/path/to/your/collectes-efs"

   # 3. Test the script
   /usr/local/bin/run-collectes.sh schedules

   # 4. Add to crontab
   crontab -e
   # Copy the lines from crontab-collectes file
```
