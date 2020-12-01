from html import unescape

"""
    We tried improving the plain text function,
    but the parsing step itself takes a ton of time.
    So, we have to re-implement it from scratch.
"""

def plain_text(
        parsed, *,
        replace_templates=True,
        replace_parser_functions=True,
        replace_parameters=True,
        replace_tags=True,
        replace_external_links=True,
        replace_wikilinks=True,
        unescape_html_entities=True,
        replace_bolds_and_italics=True,
        _is_root_node=False
    ) -> str:
        """Return a plain text string representation of self."""
        # if _is_root_node is False:
        #     s, e, m, b = self._span_data
        #     tts = self._inner_type_to_spans_copy()
        #     parsed = WikiText([self._lststr[0][s:e]], tts)
        #     parsed._span_data = tts[self._type][0]
        # else:
        #     tts = self._type_to_spans
        #     parsed = self

        tts = parsed._type_to_spans

        removeList = []

        def remove(b: int, e: int):
            removeList.append((b, e))

        for (b, e, _, _) in tts['Comment']:
            remove(b, e)
        if replace_templates:
            for (b, e, _, _) in tts['Template']:
                remove(b, e)
        if replace_parser_functions:
            for (b, e, _, _) in tts['ParserFunction']:
                remove(b, e)
        if replace_external_links:
            for el in parsed.external_links:
                if el.in_brackets:
                    b, e = el.span
                    text = el.text
                    if text is None:
                        remove(b, e)
                    else:
                        remove(b, e - 1 - len(text))
                        remove(e - 1, e)
        # replacing bold and italics should be done before wikilinks and tags
        # because removing tags and wikilinks creates invalid spans, and
        # get_bolds() will try to look into wikilinks for bold parts.
        if replace_bolds_and_italics:
            for i in parsed.get_bolds_and_italics():
                b, e = i.span
                ib, ie = i._match.span(1)  # text span
                remove(b, b + ib)
                remove(b + ie, e)
        if replace_parameters:
            for p in parsed.parameters:
                b, e = p.span
                default_start = p._shadow.find(124)
                if default_start != -1:
                    remove(b, b + default_start + 1)
                    remove(e - 3, e)
                else:
                    remove(b, e)
        if replace_tags:
            for t in parsed.get_tags():
                b, e = t.span
                cb, ce = t._match.span('contents')
                remove(b, b + cb)
                remove(b + ce, e)
        if replace_wikilinks:
            for w in parsed.wikilinks:
                b, e = w.span
                if w.wikilinks:
                    remove(b, e)  # image
                else:
                    tb, te = w._match.span(4)  # text span
                    if tb != -1:
                        remove(b, b + tb)
                        remove(b + te, e)
                    else:
                        tb, te = w._match.span(1)  # target span
                        remove(b, b + tb)
                        remove(b + te, e)

        removeList.sort()

        i = 1
        while i < len(removeList):
            if (removeList[i-1][0] == removeList[i][0]):
                removeList.pop(i-1)
                i -= 1

            i += 1

        i = 1
        while i < len(removeList):
            if (removeList[i-1][1] >= removeList[i][0]):
                newPair = (removeList[i-1][0], removeList[i][1])
                removeList[i-1] = newPair
                removeList.pop(i)
                i -= 1

            i += 1

        raw = parsed.string
        string = ""
        if (len(removeList) > 0):
            i = ri = 0
            l = len(raw)
            while i < l and ri < len(removeList):
                currentRemove = removeList[ri]
                if (i == currentRemove[0]):
                    i = currentRemove[1] - 1
                    ri += 1
                else:
                    string += raw[i]
                i += 1

            string += raw[i:]
        else:
            string = raw

        if unescape_html_entities:
            string = unescape(string)
        return string