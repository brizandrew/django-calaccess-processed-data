#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related entities derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.filings import (
    FilingMixin,
    FilingVersionMixin,
)
from calaccess_processed.models import CalAccessBaseModel
from calaccess_processed.managers import ProcessedDataManager


class Form501FilingBase(CalAccessBaseModel):
    """
    Base and abstract model for Form 501 filings.
    """
    date_filed = models.DateField(
        verbose_name='from date',
        null=True,
        db_index=True,
        help_text="Date when the Form 501 filing was filed (from F501_502_CD"
                  ".RPT_DATE)",
    )
    statement_type = models.CharField(
        max_length=62,
        verbose_name='statement type',
        help_text='Describes the type of statement, e.g. "ORIGINAL", "AMENDMENT" '
                  '(from LOOKUP_CODES.CODE_DESC)',
    )
    filer_id = models.CharField(
        verbose_name="filer identifier",
        max_length=9,
        help_text="Filer's unique identifier (from F501_502_CD.FILER_ID)",
    )
    committee_id = models.CharField(
        verbose_name='committee identifier',
        max_length=9,
        help_text="Candidate's committee's unique filer idenitifier (from "
                  "F501_502_CD.COMMITTEE_ID)",
    )
    title = models.CharField(
        verbose_name="candidate name title",
        max_length=100,
        blank=True,
        help_text="Name title of the candidate (from F501_502_CD.CAND_NAMT)",
    )
    last_name = models.CharField(
        verbose_name="candidate last name",
        max_length=200,
        # just a few don't even have a last name
        blank=True,
        help_text="Last name of the candidate (from F501_502_CD.CAND_NAML)",
    )
    first_name = models.CharField(
        verbose_name="candidate first name",
        max_length=45,
        blank=True,
        help_text="First name of the candidate (from F501_502_CD.CAND_NAMF)",
    )
    middle_name = models.CharField(
        verbose_name="candidate middle name",
        max_length=20,
        blank=True,
        help_text="Middle name of the candidate (from F501_502_CD.CAND_NAMM)",
    )
    name_suffix = models.CharField(
        verbose_name="candidate name suffix",
        max_length=10,
        blank=True,
        help_text="Name suffix of the candidate (from F501_502_CD.CAND_NAMS)",
    )
    name_moniker = models.CharField(
        verbose_name="candidate name moniker",
        max_length=20,
        blank=True,
        help_text="Moniker (aka, nickname) of the candidate (from F501_502_CD"
                  ".MONIKER)",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='candidate phone number',
        blank=True,
        help_text="Phone number of the candidate (from F501_502_CD.CAND_PHON)",
    )
    fax = models.CharField(
        max_length=20,
        verbose_name='fax number',
        blank=True,
        help_text="Phone number of the candidate (from F501_502_CD.CAND_FAX)",
    )
    email = models.CharField(
        max_length=200,
        verbose_name='email address',
        blank=True,
        help_text="Email address of the candidate (from F501_502_CD.CAND_EMAIL)",
    )
    city = models.CharField(
        max_length=200,
        verbose_name="candidate city",
        blank=True,
        help_text="City of the candidate (from F501_502_CD.CAND_CITY)",
    )
    state = models.CharField(
        max_length=200,
        verbose_name='candidate state',
        blank=True,
        help_text="State of the candidate (from F501_502_CD.CAND_ST)",
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='zip code',
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'candidate (from F501_502_CD.CAND_ZIP4)',
    )
    office = models.CharField(
        verbose_name='office sought',
        max_length=80,
        blank=True,
        help_text='Position title of the office sought by the candidate (from '
                  'LOOKUP_CODES_CD.CODE_DESC, unless NULL or 0, then F501_502_CD.'
                  'OFFICE_DSCR)',
    )
    agency = models.CharField(
        verbose_name='agency name',
        max_length=200,
        blank=True,
        help_text='Name of the agency with the office sought (from '
                  'F501_502_CD.AGENCY_NAM)',
    )
    district = models.IntegerField(
        verbose_name='district',
        null=True,
        help_text='District of office sought, if applicable (from LOOKUP_CODES_CD'
                  '.CODE_DESC, unless NULL or 0, then F501_502_CD.DIST_NO)',
    )
    party = models.CharField(
        max_length=30,
        verbose_name='political party',
        blank=True,
        help_text='Political party of the candidate (from LOOKUP_CODES_CD.'
                  'CODE_DESC, unless NULL or 0, then F501_502_CD.PARTY)',
    )

    jurisdiction = models.CharField(
        max_length=30,
        verbose_name='jurisdiction',
        blank=True,
        help_text='Jurisdiction of the office sought, e.g., "LOCAL", "STATE" '
                  '(from LOOKUP_CODES_CD.CODE_DESC)',
    )
    election_type = models.CharField(
        verbose_name='election type',
        max_length=16,
        null=True,
        help_text='Type of election in which the candidate is declaring intention'
                  ' to run, e.g. "PRIMARY", "GENERAL" (from LOOKUP_CODES_CD.'
                  'CODE_DESC)',
    )
    election_year = models.IntegerField(
        verbose_name='election year',
        null=True,
        help_text='Year in which the election is held (from F501_502_CD.YR_OF_ELEC)',
    )
    accepted_limit = models.NullBooleanField(
        null=True,
        help_text='Indicates if either the "I accept the voluntary expenditure '
                  'ceiling" or "I do not accept the voluntary expenditure" '
                  'box is checked (from F501_502_CD.ACCEPT_LIMIT_YN)',
    )
    limit_not_exceeded_election_date = models.DateField(
        verbose_name='limit not exceeded election date',
        null=True,
        help_text='Date of the primary or special election in which the candidate '
                  'did not accept the voluntary expenditure ceiling but also did '
                  'exceed the ceiling. Candidates may amend their Form 501 to accept '
                  'the limits for the general election or special election runoff '
                  'and receive all the benefits of accepting the ceiling (from '
                  'F501_502_CD.DID_EXCEED_DT)'
    )
    personal_funds_contrib_date = models.DateField(
        verbose_name='personal funds contribution date',
        null=True,
        help_text='Date on which the candidate contributed personal funds in excess '
                  'of the voluntary expenditure ceiling for the (from F501_502_CD'
                  '.CNTRB_PRSNL_FNDS_DT)',
    )
    executed_on = models.DateField(
        verbose_name='executed on date',
        null=True,
        help_text='Date on which the candidate intention statement was signed '
                  '(from F501_502_CD.EXECUTE_DT)'
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form501Filing(FilingMixin, Form501FilingBase):
    """
    The most recent version of each Form 501 filing by a candidate.

    Includes information from the most recent version of each Form 501 filing.
    All versions of the filings can be found in Form501FilingVersion.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        null=False,
        help_text='Unique identification number for the Form 501 filing ('
                  'from F501_502_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        db_index=True,
        null=False,
        help_text='Number of amendments to the Form 501 filing (from '
                  'maximum value of F501_502_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Model options.
        """
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)
        verbose_name = "Form 501 (Candidate Intention) filing"

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class Form501FilingVersion(FilingVersionMixin, Form501FilingBase):
    """
    Every version of each Form 501 (Candidate Intention Statement) filing by candidates.

    Includes information found on each version of each Form 501 filing. For the
    most recent version of each filing, see Form501Filing.
    """
    filing = models.ForeignKey(
        'Form501Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Form 501 filing ('
                  'from F501_502_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 501 filing, with 0 '
                  'representing the initial filing (from F501_502_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'amend_id',
        ),)
        index_together = ((
            'filing',
            'amend_id',
        ),)
        verbose_name = "Form 501 (Candidate Intention) filing version"

    def __str__(self):
        return '{}-{}'.format(self.filing, self.amend_id)
