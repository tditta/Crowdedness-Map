export PYTHONPATH=py
export FLASK_APP=riskmap.py
export FLASK_ENV=development

python -m flask run \
  --host=0.0.0.0 \
  --port=443 \
  --cert=/etc/letsencrypt/live/coatimundi.net/cert.pem \
  --key=/etc/letsencrypt/live/coatimundi.net/privkey.pem
