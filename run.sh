source venv/bin/activate
python cuttingStock.py >> /dev/null
if test -f "solution.last"; then
    cat solution.last
fi
