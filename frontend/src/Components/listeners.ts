function beforeUnloadListener(event: Event) {
    event.preventDefault();
    event.returnValue = true;
}

export default beforeUnloadListener;