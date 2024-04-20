# generated by datamodel-codegen:
#   filename:  api_schema.json
#   timestamp: 2024-04-20T19:18:16+00:00

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel
from pydantic import Field as PField


class GetCursor(BaseModel):
    nMode: str
    nFlag: str


class IsScriptLevelSupported(BaseModel):
    level: str


class Commit(BaseModel):
    flags: str


class CommitGetCursor(BaseModel):
    flags: str


class GetColumnIndex(BaseModel):
    pLabel: str
    flags: str


class GetColumnLabel(BaseModel):
    nCol: str
    flags: str


class GetShared(BaseModel):
    nRow: str


class SetShared(BaseModel):
    Value: str


class Execute(BaseModel):
    pszCommand: str


class Request(BaseModel):
    pszCommand: str


class SeekRow(BaseModel):
    bkOrigin: str
    nRows: str


class SetActiveDate(BaseModel):
    sDate: str
    flags: str


class SetFilter(BaseModel):
    pFilter: str
    flags: str


class SetLogic(BaseModel):
    pLogic: str
    flags: str


class SetSort(BaseModel):
    pSort: str
    flags: str


class MLValidate(BaseModel):
    pszRequiredVersion: str


class DeleteRow(BaseModel):
    nRow: str
    flags: str


class GetRowID(BaseModel):
    nRow: str
    flags: str


class GetRowTimeStamp(BaseModel):
    nRow: str
    flags: str


class FieldValue(BaseModel):
    FieldName: str


class FieldStr(BaseModel):
    field_args: str = PField(..., alias='*args')


class FieldInt(BaseModel):
    field_args: str = PField(..., alias='*args')


class Control(BaseModel):
    ControlName: str


class FieldModel(BaseModel):
    FieldName: str


class MoveToField(BaseModel):
    FieldName: str


class MoveToTab(BaseModel):
    TabName: str


class SetValue(BaseModel):
    Value: str


class Myfunction(BaseModel):
    x: str
    y: str


class GetTest(BaseModel):
    bstrVal: str


class OnClick(BaseModel):
    ControlID: str


class ClickIn(BaseModel):
    x: str
    y: str


class FieldInit(BaseModel):
    oobj: str


class FieldQueryInterface(BaseModel):
    iid: str


class OnEnterTab(BaseModel):
    Tab: str


class OnLeaveTab(BaseModel):
    Tab: str


class OnEnterField(BaseModel):
    Field: str


class OnLeaveField(BaseModel):
    Field: str


class OnEnterControl(BaseModel):
    ControlID: str


class OnLeaveControl(BaseModel):
    ControlID: str


class OnChange(BaseModel):
    ControlID: str


class OnKeyPress(BaseModel):
    ControlID: str
    KeyAscii: str


class OnActiveXControlEvent(BaseModel):
    ControlName: str
    EventName: str
    ParameterArr: str


class ComLibraryApi(BaseModel):
    GetCursor: GetCursor | None = None
    Version: dict[str, Any] | None = None
    quit: dict[str, Any] | None = None
    field__iter__: dict[str, Any] | None = PField(None, alias='__iter__')
    IsScriptLevelSupported: IsScriptLevelSupported | None = None
    Commit: Commit | None = None
    CommitGetCursor: CommitGetCursor | None = None
    GetColumnIndex: GetColumnIndex | None = None
    GetColumnLabel: GetColumnLabel | None = None
    GetShared: GetShared | None = None
    SetShared: SetShared | None = None
    Execute: Execute | None = None
    Request: Request | None = None
    SeekRow: SeekRow | None = None
    SetActiveDate: SetActiveDate | None = None
    SetFilter: SetFilter | None = None
    SetLogic: SetLogic | None = None
    SetSort: SetSort | None = None
    MLValidate: MLValidate | None = None
    DeleteRow: DeleteRow | None = None
    GetRowID: GetRowID | None = None
    GetRowTimeStamp: GetRowTimeStamp | None = None
    Clear: dict[str, Any] | None = None
    ClearAll: dict[str, Any] | None = None
    FieldValue: FieldValue | None = None
    RestoreFilter: dict[str, Any] | None = None
    field__call__: Optional[dict[str, Any]] = PField(None, alias='__call__')
    field__str__: Optional[FieldStr] = PField(None, alias='__str__')
    field__int__: Optional[FieldInt] = PField(None, alias='__int__')
    Abort: dict[str, Any] | None = None
    Cancel: dict[str, Any] | None = None
    Control: Control | None = None
    Field: FieldModel | None = None
    MoveToField: MoveToField | None = None
    MoveToTab: MoveToTab | None = None
    Save: dict[str, Any] | None = None
    SetValue: SetValue | None = None
    myfunction: Myfunction | None = None
    Test: dict[str, Any] | None = None
    Application: dict[str, Any] | None = None
    GetTest: GetTest | None = None
    GoToURL: dict[str, Any] | None = None
    HelloHTML: dict[str, Any] | None = None
    OnClick: OnClick | None = None
    clickIn: ClickIn | None = None
    field__init__: FieldInit | None = PField(None, alias='__init__')
    field__del__: dict[str, Any] | None = PField(None, alias='__del__')
    close: dict[str, Any] | None = None
    field_query_interface_: FieldQueryInterface | None = PField(
        None, alias='_query_interface_'
    )
    OnLoad: dict[str, Any] | None = None
    OnSave: dict[str, Any] | None = None
    OnCancel: dict[str, Any] | None = None
    OnEnterTab: OnEnterTab | None = None
    OnLeaveTab: OnLeaveTab | None = None
    OnEnterField: OnEnterField | None = None
    OnLeaveField: OnLeaveField | None = None
    OnEnterControl: OnEnterControl | None = None
    OnLeaveControl: OnLeaveControl | None = None
    OnChange: OnChange | None = None
    OnKeyPress: OnKeyPress | None = None
    OnActiveXControlEvent: OnActiveXControlEvent | None = None
