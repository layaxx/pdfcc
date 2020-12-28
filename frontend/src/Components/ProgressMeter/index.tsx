import 'bootstrap/dist/css/bootstrap.min.css';
import './style.css';


const paginationTexts = ["Choose PDF", "Choose Colors", "Download your new PDF!"];

function ProgressMeter(props: { progress: any, progress_enum: any }) {
    const items: JSX.Element[] = [];

    for (var i = 0; i < 3; i++) {
        items.push((<li
            key={i}
            id={"progress-" + i}
            className={"list-group-item flex-fill "
                + (i === props.progress ? "list-group-item-primary" : "")
                + (i < props.progress ? "list-group-item-secondary" : "")
            }
        > { paginationTexts[i]}</li >));
    }

    return (
        <div className="progress-wrapper">
            <ul className="list-group list-group-horizontal">{items}</ul>
        </div >
    );
}

export default ProgressMeter;

