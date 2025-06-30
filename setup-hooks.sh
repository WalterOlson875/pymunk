#!/bin/bash

# Setup script for git hooks
# Run this script to install git hooks that automate virtual environment management

echo "🔧 Setting up git hooks for Python virtual environment automation..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "💡 Run this script from the root of your git repository"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy or create the hooks
echo "📝 Installing git hooks..."

# Post-checkout hook
cat > .git/hooks/post-checkout << 'EOF'
#!/bin/bash

# Git post-checkout hook
# Automatically sets up Python virtual environment after checkout/clone

# Get the previous and new commit hashes, and whether this is a branch checkout
prev_head=$1
new_head=$2
is_branch_checkout=$3

echo "🔧 Post-checkout hook: Setting up Python environment..."

# Check if this is the initial checkout (clone)
if [ "$prev_head" = "0000000000000000000000000000000000000000" ]; then
    echo "📦 Initial clone detected - setting up virtual environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "🐍 Creating virtual environment..."
        python3 -m venv venv
        if [ $? -eq 0 ]; then
            echo "✅ Virtual environment created successfully"
        else
            echo "❌ Failed to create virtual environment"
            exit 1
        fi
    fi
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        echo "📚 Installing dependencies from requirements.txt..."
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "✅ Dependencies installed successfully"
            echo "🚀 You can now activate the environment with: source venv/bin/activate"
        else
            echo "❌ Failed to install dependencies"
            exit 1
        fi
    else
        echo "⚠️  No requirements.txt found"
    fi
    
elif [ "$is_branch_checkout" = "1" ]; then
    echo "🌿 Branch checkout detected"
    
    # Check if requirements.txt changed
    if git diff --name-only $prev_head $new_head | grep -q "requirements.txt"; then
        echo "📚 requirements.txt changed - updating dependencies..."
        if [ -d "venv" ]; then
            source venv/bin/activate
            pip install -r requirements.txt
            echo "✅ Dependencies updated"
        else
            echo "⚠️  Virtual environment not found. Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        fi
    fi
fi

echo "✨ Post-checkout hook completed"
EOF

# Post-merge hook
cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash

# Git post-merge hook
# Automatically updates Python dependencies after merge/pull

echo "🔧 Post-merge hook: Checking for dependency updates..."

# Check if requirements.txt was modified in the merge
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "requirements.txt"; then
    echo "📚 requirements.txt was updated in the merge"
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        echo "🔄 Updating dependencies..."
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo "✅ Dependencies updated successfully"
        else
            echo "❌ Failed to update dependencies"
            echo "💡 Try manually: source venv/bin/activate && pip install -r requirements.txt"
            exit 1
        fi
    else
        echo "⚠️  Virtual environment not found!"
        echo "💡 Please set up the environment:"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
    fi
else
    echo "📚 No changes to requirements.txt detected"
fi

echo "✨ Post-merge hook completed"
EOF

# Pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Git pre-commit hook
# Provides helpful checks and warnings about Python environment

echo "🔧 Pre-commit hook: Checking Python environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Warning: No virtual environment found"
    echo "💡 Consider setting up: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
fi

# Check if virtual environment is activated (in current shell context)
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment is active: $(basename $VIRTUAL_ENV)"
    
    # Check if requirements.txt exists and compare with installed packages
    if [ -f "requirements.txt" ]; then
        echo "📚 Checking if dependencies are up to date..."
        
        # Create a temporary file with current installed packages
        pip freeze > /tmp/current_packages.txt
        
        # Check if there are any differences (basic check)
        if ! pip check > /dev/null 2>&1; then
            echo "⚠️  Warning: Some package dependencies may have conflicts"
            echo "💡 Consider running: pip check"
        fi
        
        # Clean up temp file
        rm -f /tmp/current_packages.txt
    fi
else
    echo "⚠️  Virtual environment is not currently active"
    echo "💡 Consider activating it: source venv/bin/activate"
fi

# Check for Python cache files that shouldn't be committed
if find . -name "*.pyc" -o -name "__pycache__" | grep -q .; then
    echo "⚠️  Warning: Found Python cache files"
    echo "💡 These should be ignored by .gitignore"
fi

# Check if requirements.txt is being committed and suggest updating
if git diff --cached --name-only | grep -q "requirements.txt"; then
    echo "📚 requirements.txt is being committed"
    echo "💡 Make sure it reflects your current environment. You can update it with:"
    echo "   pip freeze > requirements.txt"
fi

echo "✨ Pre-commit checks completed"

# Don't block the commit, just provide warnings
exit 0
EOF

# Make hooks executable
chmod +x .git/hooks/post-checkout .git/hooks/post-merge .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
echo ""
echo "📋 Installed hooks:"
echo "  • post-checkout: Sets up venv on clone/checkout"
echo "  • post-merge: Updates dependencies after pull/merge" 
echo "  • pre-commit: Checks environment before commits"
echo ""
echo "🎉 Your repository now has automated virtual environment management!" 