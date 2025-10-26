for i in {1..10}; do
  response=$(curl -s -w "\n%{http_code}" http://localhost:8080/version)
  status=$(echo "$response" | tail -n1)
  pool=$(echo "$response" | grep -o 'X-App-Pool: [^[:space:]]*' | cut -d' ' -f2 || echo "")
  
  if [ "$status" != "200" ]; then
    echo "❌ Failed: Expected 200, got $status"
    exit 1
  fi
  
  if [[ ! "$pool" =~ "blue" ]]; then
    echo "❌ Failed: Expected Blue pool, got $pool"
    exit 1
  fi
  
  echo "✅ Request $i: 200 OK, Pool: Blue"
done
