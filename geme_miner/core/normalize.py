from enum import Enum
from dicttoxml import dicttoxml
import xml.dom.minidom
import json


class FormatTypeEnum(Enum):
    JSON = 1
    JSON_PRETTY = 2
    XML = 3
    XML_CDATA = 4
    XML_PRETTY = 5
    XML_PRETTY_CDATA = 6
    CONSOLE = 7

    def __str__(self):
        return self.name


def format_dict(
    data: dict,
    format: FormatTypeEnum,
    pretty_indent: str = " " * 4,
    consoleFormatFn: callable = None,
) -> str:
    if format == FormatTypeEnum.JSON:
        return _format_json(data)
    elif format == FormatTypeEnum.JSON_PRETTY:
        return _format_json_pretty(data)
    elif format == FormatTypeEnum.XML:
        return _format_xml(data, cdata=False)
    elif format == FormatTypeEnum.XML_CDATA:
        return _format_xml(data, cdata=True)
    elif format == FormatTypeEnum.XML_PRETTY:
        return _format_xml_pretty(data, cdata=False, indent=pretty_indent)
    elif format == FormatTypeEnum.XML_PRETTY_CDATA:
        return _format_xml_pretty(data, cdata=True, indent=pretty_indent)
    elif format == FormatTypeEnum.CONSOLE:
        return _format_console(data, consoleFormatFn)
    else:
        raise ValueError(f"Unknown format: {repr(format)}")

def _format_json(data: dict) -> str:
    return json.dumps(data)


def _format_json_pretty(data: dict) -> str:
    return json.dumps(data, indent=4)


def _format_xml(data: dict, cdata: bool = False) -> str:
    return dicttoxml(
        data,
        custom_root="data",
        cdata=cdata,
    ).decode("utf-8")


def _format_xml_pretty(
    data: dict, cdata: bool = False, indent: str = " " * 2
) -> str:
    dom = xml.dom.minidom.parseString(
        dicttoxml(
            data,
            custom_root="data",
            cdata=cdata,
        ).decode("utf-8")
    )
    return dom.toprettyxml(indent=indent)


def _format_console(data: dict, console_format_fn: callable = None) -> str:
    if console_format_fn is not None:
        return console_format_fn(data)
    return str(data)
