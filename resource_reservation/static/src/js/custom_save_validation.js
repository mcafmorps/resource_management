/** @odoo-module **/

import { useState } from '@odoo/owl';
import { FormController } from '@web/views/form/form_controller';
import { formView } from '@web/views/form/form_view';
import { registry } from '@web/core/registry';
import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog';

class CustomFormController extends FormController {
    setup() {
        super.setup();
        this.state = useState({
            unsavedChanges: false,
            isDisabled: false,
            fieldIsDirty: false,
        });
    }

    async saveButtonClicked(params = {}) {
        const saved = await super.saveButtonClicked(params);
        if (saved) {
            this.state.unsavedChanges = false;
        }
        return saved;
    }

    async beforeLeave() {
        if (this.model.root.isDirty || this.state.unsavedChanges) {
            const confirmation = await this.showUnsavedChangesDialog();
            if (!confirmation) {
                return false;
            }
        }
        return super.beforeLeave();
    }

        async discard() {
        if (this.props.discardRecord) {
            this.props.discardRecord(this.model.root);
            return;
        }
        await this.model.root.discard();
        if (this.props.onDiscard) {
            this.props.onDiscard(this.model.root);
        }
        if (this.model.root.isVirtual || this.env.inDialog) {
            this.env.config.historyBack();
        }
    }

    showUnsavedChangesDialog() {
        return new Promise((resolve) => {
            this.env.services.dialog.add(ConfirmationDialog, {
                title: "Unsaved Changes",
                body: "You have unsaved changes. Do you want to save them before leaving?",
                confirm: () => resolve(true),


                cancel: () => {
                    this.discard();
                    resolve(false);
                },
            });
        });
    }
}

registry.category('views').add('resource_reservation', {
    ...formView,
    Controller: CustomFormController,
});