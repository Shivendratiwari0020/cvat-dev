// Copyright (C) 2021 Intel Corporation
//
// SPDX-License-Identifier: MIT

(() => {
    const serverProxy = require('./server-proxy');
    const { getPreview } = require('./frames');

    const { Project } = require('./project');
    const { exportDataset, importDataset } = require('./annotations');

    function implementProject(projectClass) {
        projectClass.prototype.save.implementation = async function () {
            if (typeof this.id !== 'undefined') {
                const projectData = this._updateTrigger.getUpdated(this, {
                    bugTracker: 'bug_tracker',
                    trainingProject: 'training_project',
                    assignee: 'assignee_id',
                });
                if (projectData.assignee_id) {
                    projectData.assignee_id = projectData.assignee_id.id;
                }
                if (projectData.labels) {
                    projectData.labels = projectData.labels.map((el) => el.toJSON());
                }

                await serverProxy.projects.save(this.id, projectData);
                this._updateTrigger.reset();
                return this;
            }

            // initial creating
            const projectSpec = {
                name: this.name,
				assignee_id: this.assignee ? this.assignee.id : null,
				// catalogue_files: [...this.catalogue_files],
                // labelschema_files: [...this.labelschema_files],
                labels: this.labels.map((el) => el.toJSON()),
            };

            if (this.bugTracker) {
                projectSpec.bug_tracker = this.bugTracker;
            }

            if (this.trainingProjectCopy) {
                projectSpec.training_project = this.trainingProjectCopy;
            }

            let filesFormData = new FormData();
            this.catalogue_files.forEach((file) => {
                filesFormData.append("catalogue_files[]", file);
            });
            this.labelschema_files.forEach((file) => {
                filesFormData.append("labelschema_files[]", file);
            });

            let project = await serverProxy.projects.create(projectSpec);
            if(project){
                project = await serverProxy.projects.uploadFiles(filesFormData, project.id);
            }
            alert("Project has been successfully created.. will be redirected to projects listing");
            window.location.replace("/projects?page=1");
            return new Project(project);
        };

        projectClass.prototype.delete.implementation = async function () {
            const result = await serverProxy.projects.delete(this.id);
            return result;
        };

        projectClass.prototype.preview.implementation = async function () {
            if (!this._internalData.task_ids.length) {
                return '';
            }
            const frameData = await getPreview(this._internalData.task_ids[0]);
            return frameData;
        };

        projectClass.prototype.annotations.exportDataset.implementation = async function (
            format,
            saveImages,
            customName,
        ) {
            const result = exportDataset(this, format, customName, saveImages);
            return result;
        };
        projectClass.prototype.annotations.importDataset.implementation = async function (
            format,
            file,
            updateStatusCallback,
        ) {
            return importDataset(this, format, file, updateStatusCallback);
        };

        projectClass.prototype.backup.implementation = async function () {
            const result = await serverProxy.projects.backupProject(this.id);
            return result;
        };

        projectClass.restore.implementation = async function (file) {
            const result = await serverProxy.projects.restoreProject(file);
            return result.id;
        };

        return projectClass;
    }

    module.exports = implementProject;
})();