cd frontend
npm install
npm run build
cp build/index.html ../backend/pdfcc/templates/pdfcc
rm ../backend/pdfcc/static/js/*
rm ../backend/pdfcc/static/css/*
cp -r build/static ../backend/pdfcc