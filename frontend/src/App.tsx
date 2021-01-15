import React from 'react';
import FileUpload from './Components/FileUpload';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import ProgressMeter from './Components/ProgressMeter';
import ColorForm from './Components/ColorForm'
import Download from './Components/Download';

enum Progress {
  initial = 0,
  submittedPDF = 1,
  submittedColors = 2
}

type ComponentMap = { [key in Progress]: JSX.Element | null }

class App extends React.Component<{}, { colors: Array<Array<String>> | null, progress: Progress, file: File | null, b64: string }> {
  constructor(props: any) {
    super(props);
    this.state = {
      colors: null,
      progress: Progress.initial,
      file: null,
      b64: ""
    }
  }

  displayWarning(msg: String): void {
    alert(msg);
  }


  readonly componentsByProgress: ComponentMap = {
    [Progress.initial]:
      <FileUpload
        showColors={
          (colors: Array<Array<String>>, file: File) => {
            this.setState({ colors: colors, progress: Progress.submittedPDF, file: file });
          }} ></FileUpload >,
    [Progress.submittedPDF]:
      <ColorForm
        state={() => { return this.state; }}
        handleChange={
          (b64_in: string) => { this.setState({ b64: b64_in, progress: Progress.submittedColors }); }
        } ></ColorForm >,
    [Progress.submittedColors]:
      <Download
        b64={() => { return this.state.b64; }}
        oldFileName={() => { return this.state.file?.name }}></Download>,
  }

  render() {
    return (
      <div>
        <ProgressMeter progress_enum={Progress} progress={this.state.progress}></ProgressMeter>
        {this.componentsByProgress[this.state.progress]}
      </div>

    );
  }
}

export default App;
