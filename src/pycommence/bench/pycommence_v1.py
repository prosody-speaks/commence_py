import contextlib
import typing as _t

import pydantic as _p

from pycommence.cursor import CursorAPI, csr_context
from pycommence.exceptions import PyCommenceExistsError, PyCommenceMaxExceededError, PyCommenceNotFoundError
from pycommence.pycmc_types import FilterArray, NoneFoundHandler
from pycommence.pycommence_v2 import handle_none


class PyCommenceV1(_p.BaseModel):
    """
    Main interface for interacting with Commence.

    High-level abstraction for managing records in a Commence database table,
    including creating, reading, updating, and deleting records.

    Examples:
        Establish context and initialize PyCommence object

        >>> JEFF_KEY = 'JeffJones'
        >>> GEOFF_KEY = 'GeoffSmith'
        >>> GEOFF_DICT = {'firstName': 'Geoff', 'lastName': 'Smith', 'email': 'geoff@example.com'}
        >>> UPDATE_PKG = {'email': 'geoff.updated@example.com'}

        >>> cmc = PyCommenceV1.from_table_name('Contact')

        Get all records in the cursor

        >>> records = cmc.records()
        >>> print(records)
        [{'firstName': 'Jeff', 'lastName': 'Jones', ...}, {...}]

        Get a single record by primary key

        >>> print(cmc.one_record(),JEFF_KEY)
        {'firstName': 'Jeff', 'lastName': 'Jones', 'email': 'jeff@example.com'}

        Add a new record

        >>> cmc.add_record(pk_val=GEOFF_KEY, row_dict=GEOFF_DICT)
        True

        Modify a record

        >>> cmc.edit_record(pk_val=GEOFF_KEY, row_dict=UPDATE_PKG)
        True

        Verify the updated record

        >>> updated_geoff = cmc.one_record(),GEOFF_KEY
        >>> print(updated_geoff['email'])
        'geoff.updated@example.com'

        Delete a record

        >>> cmc.delete_record(pk_val=GEOFF_KEY)
        True

    """

    csr: CursorAPI  # Obtained from cursor.get_csr, or via PyCommence.from_table_name
    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    @property
    def row_count(self) -> int:
        return self.csr.row_count

    def get_csr(self) -> CursorAPI:
        return self.csr

    @contextlib.contextmanager
    def temporary_filter_cursor(self, filter_array: FilterArray) -> _t.Iterator[CursorAPI]:
        csr = self.get_csr()
        csr.filter_by_array(filter_array)
        yield csr
        csr.clear_all_filters()

    @classmethod
    @contextlib.contextmanager
    def from_table_name_context(
            cls,
            table_name: str,
            cmc_name: str = 'Commence.DB',
            filter_array: FilterArray | None = None,
    ) -> 'PyCommenceV1':
        """Context manager for :meth:`from_table_name`."""
        with csr_context(table_name, cmc_name, filter_array=filter_array) as csr:
            yield cls(csr=csr)

    def records(self, count: int or None = None) -> list[dict[str, str]]:
        """Return all or first `count` records from the cursor."""
        row_set = self.csr.get_query_rowset(count)
        records = row_set.get_row_dicts()
        return records

    def one_record(self, pk_val: str) -> dict[str, str]:
        """Return a single record from the cursor by primary key."""
        with self.csr.temporary_filter_pk(pk_val):
            try:
                return self.records()[0]
            except IndexError:
                raise PyCommenceNotFoundError(f'No record found for primary key {pk_val}')

    def records_by_array(self, filter_array: FilterArray, count: int | None = None) -> list[dict[str, str]]:
        """Return records from the cursor by filter array."""
        with self.csr.temporary_filter_by_array(filter_array):
            return self.records(count)

    def records_by_field(
            self,
            field_name: str,
            value: str,
            max_rtn: int | None = None,
            empty: _t.Literal['ignore', 'raise'] = 'raise'
    ) -> list[dict[str, str]]:
        """
        Get records from the cursor by field name and value.

        Args:
            field_name: Name of the field to query.
            value: Value to filter by.
            max_rtn: Maximum number of records to return. If more than this, raise CmcError.
            empty: Action to take if no records are found. Options are 'ignore', 'raise'.

        Returns:
            A list of dictionaries of field names and values for the record.

        Raises:
            CmcError:
                - If the record is not found without slecting empty='ignore',
                - If max return is not None and more than max_rtn records are found.

        """
        with self.csr.temporary_filter_fields(field_name, 'Equal To', value, none_found=empty):
            records = self.records()
            if not records and empty == 'raise':
                raise PyCommenceNotFoundError(f'No record found for {field_name} {value}')
            if max_rtn and len(records) > max_rtn:
                raise PyCommenceMaxExceededError(f'Expected max {max_rtn} records, got {len(records)}')
            return records

    def edit_record(
            self,
            pk_val: str,
            row_dict: dict,
    ) -> bool:
        """
        Modify a record.

        Args:
            pk_val (str): The value for the primary key field.
            row_dict (dict): A dictionary of field names and values to modify.

        Returns:
            bool: True on success

        """
        with self.csr.temporary_filter_pk(pk_val):
            row_set = self.csr.get_edit_rowset()
            row_set.modify_row_dict(0, row_dict)
            return row_set.commit()

    def delete_record(self, pk_val: str, none_found: NoneFoundHandler = 'raise'):
        """
        Delete a record.

        Args:
            pk_val (str): The value for the primary key field.
            none_found (str): Action to take if the record is not found. Options are 'ignore', 'raise'.

        Returns:
            bool: True on success

        """
        with self.csr.temporary_filter_pk(pk_val, none_found=none_found):
            if self.csr.row_count == 0:
                return handle_none(none_found)
            row_set = self.csr.get_delete_rowset(1)
            row_set.delete_row(0)
            res = row_set.commit()
            return res

    def delete_multiple(
            self, *, pk_vals: list[str], max_delete: int | None = 1, empty: NoneFoundHandler = 'raise'
    ):
        """
        Delete multiple records.

        Args:
            pk_vals (list): A list of primary key values.
            empty (str): Action to take if a record is not found. Options are 'ignore', 'raise'.
            max_delete (int): Maximum number of records to delete. If less than the number of records to delete, raise CmcError. Set None to disabl safety check

        Returns:
            bool: True on success

        """
        if max_delete and len(pk_vals) > max_delete:
            raise PyCommenceMaxExceededError(
                f'max_delete ({max_delete}) is less than the number of records to delete ({len(pk_vals)})'
            )
        for pk_val in pk_vals:
            self.delete_record(pk_val, none_found=empty)

    def add_record(
            self, pk_val: str, row_dict: dict[str, str], existing: _t.Literal['replace', 'update', 'raise'] = 'raise'
    ) -> bool:
        """
        Add a record.

        Args:
            pk_val: The value for the primary key field.
            row_dict: A dictionary of field names and values to add to the record.
            existing: Action to take if the record already exists. Options are 'replace', 'update', 'raise'.

        Returns:
            bool: True on success

        """
        with self.csr.temporary_filter_pk(pk_val, none_found='ignore'):  # noqa: PyArgumentList
            if not self.csr.row_count:
                row_set = self.csr.get_named_addset(pk_val)
            else:
                if existing == 'raise':
                    raise PyCommenceExistsError('Record already exists')
                elif existing == 'update':
                    row_set = self.csr.get_edit_rowset()
                elif existing == 'replace':
                    self.delete_record(pk_val)
                    row_set = self.csr.get_named_addset(pk_val)

            row_set.modify_row_dict(0, row_dict)
            res = row_set.commit()
            return res
