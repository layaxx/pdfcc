# PDF Color Changer
## Python and React-based webapp allowing substitution of colors in a PDF.
This is a proof-of-concept. 

It is provided as-is and there will probably not be any major updates in the future.

# About this project

  - [Motivation](#motivation)
  - [What PDFCC can do](#what-pdfcc-can-do)
  - [What PDFCC cannot do](#what-pdfcc-cannot-do)
  - [How PDFCC works](#how-pdfcc-works)
    - [General Mode of Operation](#general-mode-of-operation)
    - [Frontend](#frontend)
    - [Backend](#backend)
    - [Hosting](#hosting)
  - [Privacy](#privacy)
  - [Plans for the Future](#plans-for-the-future)

## Motivation
The idea for this project came to me when a fellow student asked our professor if he could provide an alternate version of the presentation slides. The original version had white text on a dark background, which meant that printing them was a waste of toner. The professor then stated that he did not know a way to automate the task, which got me curious. After a few days I had the first prototype ready: It certainly did not automate the entire job, but it did make it easier than manual adjustments.

## What PDFCC can do
PDF Color Changer can detect colors that are used in a PDF, for example as font color, background color or color of objects.
Every Color that was found is then listed, together with a list of the pages it appeared on,  sorted by the amount of pages. This means that a
color, that is found on every page will be on top, whereas a color that only appeared on one page will be at the bottom. For every color that was found, you can then specify a new color, which will replace every instance of the old color.

## What PDFCC cannot do
The PDF format allows for pictures to be embedded on sites. These are (currently) ignored by PDFCC. This means, that colors, that are only used inside of pictures in a given PDF will not be displayed by the app. Colors inside pictures will therefore also not be substituted.
In some cases, substitution causes elements to become invisible. In that case you will have to edit the Document manually, for example with Adobe Acrobat.

## How PDFCC works
### General Mode of Operation
This App makes use of the way the PDF format works. If you got time on your hands and are interested in learning more about PDF, you should take a look at this document: [Adobe´s PDF (1.7) Specification](https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf), especially section A2. Please note that this is not the latest PDF Specification, there is a Version 2.0, but in contrast to the Specification linked above the new one is not freely accessible. I plan on writing a Blog post going more into detail about this project.
### Frontend
The Frontend is written in React (Typescript).
### Backend
The Backend is written in Django (Python).
### Hosting
This webapp is hosted on a free-tier instance of heroku and is accessible under [pdfcc.herokuapp.com](http://pdfcc.herokuapp.com).
Due to the limitations of the free tier, loading the app may take a few seconds.

## Privacy
This app does not collect any personal information. It does not use cookies, neither for tracking or advertising, nor for other purposes.
Submitted files are only stored in-memory and only for the duration of the substitution process.

## Plans for the future
As stated previously, there will probably not be any major updates. However I do plan to add unit tests to the backend and possibly the frontend as well.
