echo "Starting All Microservices..."
sh scripts/run_account.sh &
sh scripts/run_transaction.sh &
sh scripts/run_topup.sh &
echo "All microservices run in the background."