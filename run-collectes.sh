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
    local task_args="$2"
    local log_file="$LOG_DIR/${task_name}_${task_args//-/}-$(date '+%Y%m%d_%H%M%S').log"
   
    log "Starting $task_name with args: $task_args"
   
    cd "$PROJECT_DIR" || {
        log "ERROR: Cannot access directory $PROJECT_DIR"
        exit 1
    }
   
    # Execute task - pass arguments after the service name
    if [ -n "$task_args" ]; then
        docker compose run --rm "$task_name" "$task_args" 2>&1 | tee "$log_file"
    else
        docker compose run --rm "$task_name" 2>&1 | tee "$log_file"
    fi
    local exit_code=$?
   
    if [ $exit_code -eq 0 ]; then
        log "✅ $task_name completed successfully"
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
    "groups")
        log "=== GROUPS COLLECTION ==="
        run_task "cli" "--groups"
        ;;

    "locations")
        log "=== LOCATIONS COLLECTION ==="
        run_task "cli" "--locations"
        ;;
    
    "collections")
        log "=== COLLECTIONS COLLECTION ==="
        run_task "cli" "--collections"
        ;;
    
    "schedules")
        log "=== SCHEDULES COLLECTION ==="
        run_task "cli" "--schedules"
        ;;
    
    *)
        echo "Usage: $0 {groups|locations|collections|schedules}"
        echo ""
        echo "Examples:"
        echo "  $0 schedules    # Run only get-schedules"
        exit 1
        ;;
esac

log "Script completed"