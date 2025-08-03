#!/bin/bash

# =============================================================================
# EFS Collections Launch Script
# =============================================================================

# Configuration
PROJECT_DIR="/path/to/your/collectes-efs"  # Update with your path
LOG_DIR="$PROJECT_DIR/logs"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$DATE] $1" | tee -a "$LOG_DIR/collectes.log"
}

# Function to execute a Docker Compose task
run_task() {
    local task_name="$1"
    local log_file="$LOG_DIR/${task_name}_$(date '+%Y%m%d_%H%M%S').log"
    
    log "Starting $task_name"
    
    cd "$PROJECT_DIR" || {
        log "ERROR: Cannot access directory $PROJECT_DIR"
        exit 1
    }
    
    # Execute task with 30-minute timeout
    timeout 1800 docker compose run --rm "$task_name" 2>&1 | tee "$log_file"
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log "✅ $task_name completed successfully"
    elif [ $exit_code -eq 124 ]; then
        log "⏰ $task_name interrupted (30min timeout)"
    else
        log "❌ $task_name failed (code: $exit_code)"
    fi
    
    return $exit_code
}

# Check if Docker is accessible
if ! docker info >/dev/null 2>&1; then
    log "❌ ERROR: Docker is not accessible"
    exit 1
fi

# Check if project exists
if [ ! -f "$PROJECT_DIR/compose.yaml" ]; then
    log "❌ ERROR: compose.yaml file not found in $PROJECT_DIR"
    exit 1
fi

# Execute task based on parameter
case "${1:-}" in
    "locations")
        log "=== LOCATIONS COLLECTION ==="
        run_task "get-locations"
        ;;
    
    "collections")
        log "=== COLLECTIONS COLLECTION ==="
        run_task "get-collections"
        ;;
    
    "schedules")
        log "=== SCHEDULES COLLECTION ==="
        run_task "get-schedules"
        ;;
    
    *)
        echo "Usage: $0 {locations|collections|schedules|all}"
        echo ""
        echo "Examples:"
        echo "  $0 schedules    # Run only get-schedules"
        echo "  $0 all          # Run all collections"
        exit 1
        ;;
esac

log "Script completed"