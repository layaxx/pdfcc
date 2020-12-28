cd frontend
npm install
npm run build
cp build/index.html ../backend/pdfcc/templates/pdfcc
cp -r build/static ../backend/pdfcc