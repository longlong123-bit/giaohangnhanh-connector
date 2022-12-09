/** @odoo-module */

import { listView } from "@web/views/list/list_view";
import { ButtonListModel } from "./ButtonListModel";
import { ButtonListController } from "./ButtonListController";
import { registry } from "@web/core/registry";

export const ButtonListView = {
    ...listView,
    Model: ButtonListModel,
    Controller: ButtonListController,
    buttonTemplate: 'Sync.Buttons',
};

registry.category("views").add('override_btn', ButtonListView);