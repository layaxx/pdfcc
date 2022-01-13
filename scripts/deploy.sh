cp ./frontend/build/index.html ./backend/pdfcc/templates/pdfcc
rm ./backend/pdfcc/static/js/*
rm ./backend/pdfcc/static/css/*
cp -r ./frontend/build/static ./backend/pdfcc