#!/usr/bin/env bash
# welcome.sh - Dev container welcome script

cat << 'EOF'
🚀 PydanticAI API Template Development Environment

Available commands:
  • start     - Start the development server (pydanticai-api-template run --reload)
  • validate  - Check environment configuration
  • lint      - Run code quality checks
  • test      - Run test suite
  • sync      - Synchronize configuration files

Quick start:
  1. Run 'start' or press Cmd+Shift+B to start the server
  2. Visit http://localhost:8000/docs for API documentation

For more information, see the documentation in ./docs/
EOF

# Check if this is the first run
WELCOME_FLAG="$HOME/.welcome_shown"
if [ ! -f "$WELCOME_FLAG" ]; then
    # Create the flag file to prevent showing welcome message again in the same session
    touch "$WELCOME_FLAG"

    # Print additional first-run information
    echo ""
    echo "✨ First time in this container? Try these commands:"
    echo "   - 'check' to verify your environment"
    echo "   - 'help' to see all available aliases"
    echo ""
    echo "⚠️  Server is NOT automatically started for better stability."
    echo "   - Run 'start' when you're ready to launch the server"
    echo "   - Use Ctrl+C to stop the server if needed"
fi
