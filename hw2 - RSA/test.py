#!/usr/bin/env python


def exp(m, e, p):
    return (m ** e) % p


def test(m, e, d, p):
    y = exp(m, e, p)
    x = exp(y, d, p)
    print 'message:', m, 'encrypted:', y, 'decrypted:', x
