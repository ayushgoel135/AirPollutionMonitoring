// Controls for the 3D visualization
class VisualizationControls {
    constructor(camera, renderer) {
        this.camera = camera;
        this.renderer = renderer;
        this.controls = new THREE.OrbitControls(camera, renderer.domElement);
        this.init();
    }

    init() {
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.25;
        this.controls.screenSpacePanning = false;
        this.controls.maxPolarAngle = Math.PI;
        this.controls.minDistance = 3;
        this.controls.maxDistance = 10;
    }

    update() {
        this.controls.update();
    }

    handleResize() {
        const container = document.getElementById('visualization-container');
        this.camera.aspect = container.clientWidth / container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(container.clientWidth, container.clientHeight);
    }

    zoomIn() {
        this.camera.fov -= 5;
        this.camera.updateProjectionMatrix();
    }

    zoomOut() {
        this.camera.fov += 5;
        this.camera.updateProjectionMatrix();
    }

    toggleAutoRotate() {
        this.controls.autoRotate = !this.controls.autoRotate;
    }
}

export default VisualizationControls;