// Load highlight.js
var s = document.createElement("script");
s.src = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.2.0/highlight.min.js";
s.onload = function () {
    // Register dax as a custom language for highlight.js
    hljs.registerLanguage('dax', function (hljs) {
        var IDENT_RE = '[a-zA-Z][a-zA-Z0-9._]*';
        return {
            case_insensitive: true,
            contains: [
                hljs.C_LINE_COMMENT_MODE,
                hljs.C_BLOCK_COMMENT_MODE,
                {
                    begin: IDENT_RE,
                    lexemes: IDENT_RE,
                    keywords: {
                        keyword:
                            'ABS ACOS ACOSH ADDCOLUMNS ADDMISSINGITEMS ALL ALLEXCEPT ALLNOBLANKROW ' +
                            'ALLSELECTED AND ASIN ASINH ATAN ATANH AVERAGE AVERAGEA AVERAGEX BETA.DIST ' +
                            'BETA.INV BLANK CALCULATE CALCULATETABLE CALENDAR CALENDARAUTO CEILING ' +
                            'CHISQ.INV CHISQ.INV.RT CLOSINGBALANCEMONTH CLOSINGBALANCEQUARTER ' +
                            'CLOSINGBALANCEYEAR CODE COMBIN COMBINA CONCATENATE CONCATENATEX ' +
                            'ABS ACOS ACOSH ADDCOLUMNS ADDMISSINGITEMS|10 ALL ALLEXCEPT|10 ALLNOBLANKROW|10 ' +
                            'ALLSELECTED|10 AND ASIN ASINH ATAN ATANH AVERAGE AVERAGEA AVERAGEX BETA.DIST ' +
                            'BETA.INV BLANK CALCULATE CALCULATETABLE|10 CALENDAR CALENDARAUTO|10 CEILING ' +
                            'CHISQ.INV CHISQ.INV.RT CLOSINGBALANCEMONTH|10 CLOSINGBALANCEQUARTER|10 ' +
                            'CLOSINGBALANCEYEAR|10 CODE COMBIN COMBINA CONCATENATE CONCATENATEX ' +
                            'CONFIDENCE.NORM CONFIDENCE.T CONTAINS COS COSH COUNT COUNTA COUNTAX ' +
                            'COUNTBLANK COUNTROWS COUNTX CROSSFILTER CURRENCY CUSTOMDATA DATATABLE ' +
                            'DATE DATEADD DATEDIFF DATESBETWEEN DATESINPERIOD DATESMTD DATESQTD ' +
                            'DATESYTD DATEVALUE DAY DEGREES DISTINCT DISTINCTCOUNT DIVIDE EARLIER ' +
                            'EARLIEST EDATE ENDOFMONTH ENDOFQUARTER ENDOFYEAR EOMONTH EVALUATE EVEN EXACT EXCEPT ' +
                            'EXP EXPON.DIST FACT FILTER FILTERS FIND FIRSTDATE FIRSTNONBLANK FIXED ' +
                            'FLOOR FORMAT GCD GENERATEALL GEOMEAN GEOMEANX GROUPBY HASONEFILTER ' +
                            'HASONEVALUE HOUR IF IFERROR IN INT INTERSECT ISBLANK ISCROSSFILTERED ISEMPTY ' +
                            'ISERROR ISEVEN ISFILTERED ISLOGICAL ISNONTEXT ISNUMBER ISO.CEILING ISODD ' +
                            'ISONORAFTER ISTEXT KEEPFILTERS LASTDATE LASTNONBLANK LCM LEFT LEN LN LOG ' +
                            'LOOKUPVALUE LOWER MAX MAXA MAXX MEDIAN MEDIANX MID MIN MINA MINUTE MINX ' +
                            'MOD MONTH MROUND NATURALINNERJOIN NATURALLEFTOUTERJOIN NEXTDAY NEXTMONTH ' +
                            'NEXTQUARTER NEXTYEAR NOT NOW ODD OPENINGBALANCEMONTH OPENINGBALANCEQUARTER ' +
                            'OPENINGBALANCEYEAR OR ORDER BY PARALLELPERIOD PATH PATHCONTAINS PATHITEM ' +
                            'PATHITEMREVERSE PATHLENGTH PERCENTILE.EXC PERCENTILE.INC PERCENTILEX.EXC ' +
                            'PERCENTILEX.INC PERMUT PI POISSON.DIST POWER PREVIOUSDAY PREVIOUSMONTH ' +
                            'PREVIOUSQUARTER PREVIOUSYEAR PRODUCT PRODUCTX QUOTIENT RADIANS RAND ' +
                            'RANDBETWEEN RANKX RELATED RELATEDTABLE REPLACE REPT RIGHT ROUND ROUNDDOWN ' +
                            'ROUNDUP ROW SAMEPERIODLASTYEAR SAMPLE SEARCH SECOND SELECTCOLUMNS SIGN ' +
                            'SIN SINH SQRT SQRTPI STARTOFMONTH STARTOFQUARTER STARTOFYEAR STDEV.P ' +
                            'STDEV.S STDEVX.P STDEVX.S SUBSTITUTE SUBSTITUTEWITHINDEX SUM SUMMARIZE ' +
                            'SUMMARIZECOLUMNS SUMX SWITCH TAN TANH TIME TIMEVALUE TODAY TOPN TOTALMTD ' +
                            'TOTALQTD TOTALYTD TRIM TRUNC UNION UPPER USERELATIONSHIP USERNAME VALUE ' +
                            'VALUES VAR.P VAR.S VARX.P VARX.S WEEKDAY WEEKNUM XIRR XNPV YEAR YEARFRAC ' +
                            'COUNTBLANK|10 COUNTROWS COUNTX CROSSFILTER|10 CROSSJOIN|10 CURRENCY CUSTOMDATA ' +
                            'DATATABLE|10 DATE DATEADD DATEDIFF DATESBETWEEN|10 DATESINPERIOD|10 DATESMTD ' +
                            'DATESQTD|10 DATESYTD|10 DATEVALUE DAY DEGREES DISTINCT DISTINCTCOUNT DIVIDE ' +
                            'EARLIER EARLIEST EDATE ENDOFMONTH|10 ENDOFQUARTER|10 ENDOFYEAR|10 EOMONTH|10 EVEN ' +
                            'EXACT EXCEPT EXP EXPON.DIST FACT FILTER FILTERS FIND FIRSTDATE ' +
                            'FIRSTNONBLANK|10 FIXED FLOOR FORMAT GCD GENERATE GENERATEALL GEOMEAN ' +
                            'GEOMEANX GROUPBY HASONEFILTER|10 HASONEVALUE|10 HOUR IF IFERROR INT INTERSECT ' +
                            'ISBLANK|10 ISCROSSFILTERED|10 ISEMPTY ISERROR ISEVEN ISFILTERED ISLOGICAL ' +
                            'ISNONTEXT ISNUMBER ISO.CEILING ISODD ISONORAFTER ISTEXT KEEPFILTERS ' +
                            'LASTDATE LASTNONBLANK|10 LCM LEFT LEN LN LOG LOG10 LOOKUPVALUE|10 LOWER MAX ' +
                            'MAXA MAXX MEDIAN MEDIANX MID MIN MINA MINUTE MINX MOD MONTH MROUND ' +
                            'NATURALINNERJOIN|10 NATURALLEFTOUTERJOIN|10 NEXTDAY|10 NEXTMONTH|10 NEXTQUARTER|10 ' +
                            'NEXTYEAR|10 NOT NOW ODD OPENINGBALANCEMONTH|10 OPENINGBALANCEQUARTER|10 ' +
                            'OPENINGBALANCEYEAR|10 OR PARALLELPERIOD|10 PATH PATHCONTAINS|10 PATHITEM|10 ' +
                            'PATHITEMREVERSE|10 PATHLENGTH|10 PERCENTILE.EXC PERCENTILE.INC PERCENTILEX.EXC ' +
                            'PERCENTILEX.INC PERMUT PI POISSON.DIST POWER PREVIOUSDAY|10 PREVIOUSMONTH|10 ' +
                            'PREVIOUSQUARTER|10 PREVIOUSYEAR|10 PRODUCT PRODUCTX QUOTIENT RADIANS RAND ' +
                            'RANDBETWEEN RANK.EQ RANKX RELATED RELATEDTABLE|10 REPLACE REPT RIGHT ROUND ' +
                            'ROUNDDOWN ROUNDUP ROW SAMEPERIODLASTYEAR|10 SAMPLE SEARCH SECOND SIGN SIN ' +
                            'SINH SQRT SQRTPI STARTOFMONTH|10 STARTOFQUARTER|10 STARTOFYEAR|10 STDEV.P STDEV.S ' +
                            'STDEVX.P STDEVX.S SUBSTITUTE SUBSTITUTEWITHINDEX|10 SUM SUMMARIZE ' +
                            'SUMMARIZECOLUMNS|10 SUMX SWITCH TAN TANH TIME TIMEVALUE TODAY TOPN TOTALMTD|10 ' +
                            'TOTALQTD|10 TOTALYTD|10 TRIM TRUNC UNION UPPER USERELATIONSHIP|10 USERNAME VALUE ' +
                            'VALUES VAR.P VAR.S VARX.P VARX.S WEEKDAY WEEKNUM XIRR|10 XNPV|10 YEAR YEARFRAC|10 ' +
                            'FALSE TRUE VAR RETURN'
                    },
                    relevance: 0
                },
                {
                    className: 'string',
                    begin: '"', end: '"',
                    contains: [
                        {
                            begin: '""'
                        }
                    ],
                    relevance: 0
                },
                {
                    className: 'number',
                    begin: '((\\b\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]?\\d+)?)',
                    relevance: 0
                },
                {
                    // quoted identifier
                    begin: '\'',
                    end: '\'',
                    illegal: '\\.,;:/\\\\\\*\\|\\?&%\\$!\\+=\\(\\)\\[\\]\\{\\}<>',
                    relevance: 0
                },
                {
                    // enclosed identifier
                    begin: '\\[',
                    end: '\\]',
                    illegal: '\\.,;:/\\\\\\*\\|\\?&%\\$!\\+=\\(\\)\\[\\]\\{\\}<>',
                    relevance: 0
                }
            ]
        };
    }
    );
    // Highlight the DAX code
    $('code.lang-dax').each(function (i, block) {
        hljs.highlightBlock(block);
    });
    $(function () {
        var copyToClipboard = function (text) {
            // Create a textblock and assign the text and add to document
            var el = document.createElement('textarea');
            el.value = text;
            document.body.appendChild(el);
            el.style.display = "block";

            // select the entire textblock
            if (window.document.documentMode)
                el.setSelectionRange(0, el.value.length);
            else
                el.select();

            // copy to clipboard
            document.execCommand('copy');

            // clean up element
            document.body.removeChild(el);
        }

        $("code.hljs").each(function () {
            var $this = $(this);
            var language = /lang-(.+?)(\s|$)/.exec($this.attr("class"))[1].toUpperCase();
            if (language === 'CSHARP') {
                language = "C#";
            }
            if (language === 'M') {
                language = "POWER QUERY";
            }
            var $codeHeader = $(
                '<div class="code-header">' +
                '    <span class="language">' + language + '</span>' +
                '    <button type="button" class="action" aria-label="Copy code">' +
                '		<span class="icon"><span class="glyphicon glyphicon-duplicate" role="presentation"></span></span>' +
                '		<span>Copy</span>' +
                '		<div class="successful-copy-alert is-transparent" aria-hidden="true">' +
                '			<span class="icon is-size-large">' +
                '				<span class="glyphicon glyphicon-ok" role="presentation"></span>' +
                '			</span>' +
                '		</div>' +
                '	</button>' +
                '</div>'
            );

            // Create the code container element
            var $codeContainer = $this.closest("pre").wrap('<div class="code-container"></div>').parent();

            // Check if there are any tabGroups on the page
            var tabGroups = $(".tabGroup");
            // Check if there are any tabGroups on the page
            if (tabGroups.length > 0) {
                // Only add the code header element before the code container if it is inside a tabGroup
                var $parentTab = $codeContainer.closest('[role="tabpanel"]');
                if ($parentTab.length > 0) {
                    $codeHeader.insertBefore($codeContainer);
                }

            } else {
                // If there are no tabGroups, add the code header element before the code container
                $codeContainer.before($codeHeader);
            };

            $codeHeader.find("button").click(function () {
                copyToClipboard($this.closest("pre").text());
                var successAlert = $(this).find(".successful-copy-alert");
                successAlert.removeClass("is-transparent");
                setTimeout(function () { successAlert.addClass("is-transparent"); }, 2000);
            });
        });
    });

};
document.head.appendChild(s);

$(function () {
    var copyToClipboard = function (text) {
        // Create a textblock and assign the text and add to document
        var el = document.createElement('textarea');
        el.value = text;
        document.body.appendChild(el);
        el.style.display = "block";

        // select the entire textblock
        if (window.document.documentMode)
            el.setSelectionRange(0, el.value.length);
        else
            el.select();

        // copy to clipboard
        document.execCommand('copy');

        // clean up element
        document.body.removeChild(el);
    }

    $("code.hljs").each(function () {
        var $this = $(this);
        var language = /lang-(.+?)(\s|$)/.exec($this.attr("class"))[1].toUpperCase();
        if (language === 'CSHARP') {
            language = "C#";
        }
        if (language === 'M') {
            language = "POWER QUERY";
        }
        var $codeHeader = $(
            '<div class="code-header">' +
            '    <span class="language">' + language + '</span>' +
            '    <button type="button" class="action" aria-label="Copy code">' +
            '		<span class="icon"><span class="glyphicon glyphicon-duplicate" role="presentation"></span></span>' +
            '		<span>Copy</span>' +
            '		<div class="successful-copy-alert is-transparent" aria-hidden="true">' +
            '			<span class="icon is-size-large">' +
            '				<span class="glyphicon glyphicon-ok" role="presentation"></span>' +
            '			</span>' +
            '		</div>' +
            '	</button>' +
            '</div>'
        );

        // Create the code container element
        var $codeContainer = $this.closest("pre").wrap('<div class="code-container"></div>').parent();

        // Check if there are any tabGroups on the page
        var tabGroups = $(".tabGroup");
        // Check if there are any tabGroups on the page
        if (tabGroups.length > 0) {
            // Only add the code header element before the code container if it is inside a tabGroup
            var $parentTab = $codeContainer.closest('[role="tabpanel"]');
            if ($parentTab.length > 0) {
                $codeHeader.insertBefore($codeContainer);
            }

        } else {
            // If there are no tabGroups, add the code header element before the code container
            $codeContainer.before($codeHeader);
        };

        $codeHeader.find("button").click(function () {
            copyToClipboard($this.closest("pre").text());
            var successAlert = $(this).find(".successful-copy-alert");
            successAlert.removeClass("is-transparent");
            setTimeout(function () { successAlert.addClass("is-transparent"); }, 2000);
        });
    });
});