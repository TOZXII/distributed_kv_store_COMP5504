if [ "$SERVICE" = "flask" ]; then
    
    flask run --host=0.0.0.0 --port=5000
elif [ "$SERVICE" = "node" ]; then
    
    python nodes/node.py $NODE_ID
else
    echo "Invalid service specified"
    exit 1
fi
