import React, { ChangeEvent, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Spinner from 'react-bootstrap/Spinner';
import './style.css';


function FileUpload(prop: { showColors: (colorArray: Array<Array<String>>, file: File) => void }) {
    const [isValid, setIsValid] = useState(false);
    const [file, setFile] = useState({});
    const [alertState, setAlertState] = useState({ message: "", type: "" });

    function fileIsValid(event: ChangeEvent): Boolean {
        const fileSize: number | undefined = (event?.target as HTMLInputElement)?.files?.item(0)?.size;
        if (typeof fileSize === "undefined") {
            return false;
        } else if (typeof fileSize === "number") {
            if (fileSize > 15728640) {
                setAlertState({ message: "The size of the PDF must be 15 MB or less", type: "warning" });
                return false;
            } else {
                return true;
            }
        }
        return false;
    }

    return (
        <div>
            <h4 className="mb-3">PDF Document</h4>
            <form encType="multipart/form-data" id="id_ajax_upload_form" method="POST" noValidate>
                <label htmlFor="input_pdf">Choose a PDF Document: </label>
                <br />
                <input id="input_pdf" type="file" accept="application/pdf" onChange={(e) => {
                    if (fileIsValid(e) && e.target.files != null) {
                        setFile(e.target.files[0])
                        setIsValid(true);
                        setAlertState({ message: "", type: "" });
                    } else {
                        setIsValid(false);
                        (document.getElementById("id_ajax_upload_form") as HTMLFormElement)?.reset();
                    }
                }} required></input>
                <div className="status-wrapper">
                    <Alert
                        variant={alertState.type}
                        id="submit-status"
                        hidden={alertState.type === ""}>
                        <Spinner
                            animation="border"
                            role="status"
                            hidden={alertState.message !== "Waiting for Server response"}></Spinner>
                        {alertState.message}</Alert>
                </div>
                <Button id="submit-pdf" type="submit" block onClick={(event: React.MouseEvent) => {
                    event.preventDefault();
                    if (isValid) {
                        var data: FormData = new FormData();
                        const pdf = file as Blob;
                        data.append('file', pdf);
                        setAlertState({ message: "Waiting for Server response", type: "info" });
                        fetch("/ajax/react", {
                            method: 'POST',
                            body: data
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw Error(response.statusText);
                                }
                                return response;
                            })
                            .then(response => response.json())
                            .then(response => {
                                if (response.error) {
                                    setAlertState({ message: "Server responded with error message: " + response.message, type: "danger" });
                                } else {
                                    prop.showColors(response.analysis_result, file as File);
                                }

                            })
                            .catch(function (error) {
                                setAlertState({ message: error, type: "danger" });
                            });
                    } else {
                        setAlertState({ message: "Please select a Document first", type: "warning" });
                    }
                }}
                    disabled={alertState.message === "Waiting for Server response"}>
                    {alertState.message !== "Waiting for Server response" ? "Submit Document" : "Waiting..."}
                </Button>
            </form>
        </div >
    );
}

export default FileUpload;