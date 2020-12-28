import 'bootstrap/dist/css/bootstrap.min.css';

function Download(props: { b64: () => string, oldFileName: () => string | undefined }) {
    const oldFileName = props.oldFileName();
    const newFileName = oldFileName?.split(".pdf")[0] + "-printable";
    return (
        <div>
            <h4 className="mb-3">PDF Document</h4>
            <a
                href={"data:application/pdf;base64," + props.b64()}
                className="btn btn-success btn-block" download={newFileName}>
                Download your new PDF!
                </a>
        </div >
    );
}

export default Download;