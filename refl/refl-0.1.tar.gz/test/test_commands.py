#!/usr/bin/env python3

import pytest
import sys
sys.path.insert(0, '.')

from src.commands import *
from src.log import Logging

def test_range():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)
  assert r() == '(intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ])'

def test_compile():
  assert Commands('./test/test.agda').compile('GHC', []) == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_compile GHC "./test/test.agda" [])'

def test_load():
  assert Commands('./test/test.agda').load([]) == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_load "./test/test.agda" [])'

def test_constraints():
  assert Commands('./test/test.agda').constraints() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_constraints)'

def test_metas():
  assert Commands('./test/test.agda').metas() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_metas)'

def test_show_module_contents_toplevel():
  assert Commands('./test/test.agda').show_module_contents_toplevel('Normalised', 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" None Indirect (Cmd_show_module_contents_toplevel Normalised "Agda.Builtin.Nat")'

def test_search_about_toplevel():
  assert Commands('./test/test.agda').search_about_toplevel('Normalised', 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_search_about_toplevel Normalised "Agda.Builtin.Nat")'

def test_solveAll():
  assert Commands('./test/test.agda').solveAll('Normalised') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_solveAll Normalised)'

def test_solveOne():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)

  assert Commands('./test/test.agda').solveOne('Normalised', 0, r, 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_solveOne Normalised 0 (intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ]) "Agda.Builtin.Nat")'

def test_autoAll():
  assert Commands('./test/test.agda').autoAll() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_autoAll)'

def test_autoOne():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)

  assert Commands('./test/test.agda').autoOne(0, r, 'Agda.Builtin.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_autoOne 0 (intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ]) "Agda.Builtin.Nat")'

def test_auto():
  r = Range()

  assert Commands('./test/test.agda').auto(0, r, '') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_auto 0 noRange "")'

def test_infer_toplevel():
  assert Commands('./test/test.agda').infer_toplevel('Normalised', 'Agda.Builtin.Nat.Nat') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_infer_toplevel Normalised "Agda.Builtin.Nat.Nat")'

def test_compute_toplevel():
  assert Commands('./test/test.agda').compute_toplevel('DefaultCompute', 'suc zero') == \
    'IOTCM "./test/test.agda" None Indirect (Cmd_compute_toplevel DefaultCompute "suc zero")'

def test_load_highlighting_info():
  assert Commands('./test/test.agda').load_highlighting_info() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_load_highlighting_info "./test/test.agda")'

def test_tokenHighlighting():
  assert Commands('./test/test.agda').tokenHighlighting('Keep') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_tokenHighlighting "./test/test.agda" Keep)'

def test_highlight():
  r = rangeBuilder('./test/test.agda', 6, 6, 8, 6, 6, 12)

  assert Commands('./test/test.agda').highlight(0, r) == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_highlight 0 (intervalsToRange (Just (mkAbsolute "./test/test.agda")) [Interval  (Pn () 6 6 8 ) (Pn () 6 6 12 ) ]) "./test/test.agda")'

def test_give():
  assert Commands('./test/test.agda').give('WithoutForce', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_give WithoutForce 0 noRange "proof₁")'

def test_refine():
  assert Commands('./test/test.agda').refine(0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_refine 0 noRange "proof₁")'

def test_intro():
  assert Commands('./test/test.agda').intro(True, 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_intro True 0 noRange "proof₁")'

def test_refine_or_intro():
  assert Commands('./test/test.agda').refine_or_intro(True, 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_refine_or_intro True 0 noRange "proof₁")'

def test_context():
  assert Commands('./test/test.agda').context('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_context Simplified 0 noRange "proof₁")'

def test_helper_function():
  assert Commands('./test/test.agda').helper_function('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_helper_function Simplified 0 noRange "proof₁")'

def test_infer():
  assert Commands('./test/test.agda').infer('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_infer Simplified 0 noRange "proof₁")'

def test_goal_type():
  assert Commands('./test/test.agda').goal_type('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_goal_type Simplified 0 noRange "proof₁")'

def test_elaborate_give():
  assert Commands('./test/test.agda').elaborate_give('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_elaborate_give Simplified 0 noRange "proof₁")'

def test_goal_type_context():
  assert Commands('./test/test.agda').goal_type_context('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_goal_type_context Simplified 0 noRange "proof₁")'

def test_goal_type_context_infer():
  assert Commands('./test/test.agda').goal_type_context_infer('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_goal_type_context_infer Simplified 0 noRange "proof₁")'

def test_goal_type_context_check():
  assert Commands('./test/test.agda').goal_type_context_check('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_goal_type_context_check Simplified 0 noRange "proof₁")'

def test_show_module_contents():
  assert Commands('./test/test.agda').show_module_contents('Simplified', 0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_show_module_contents Simplified 0 noRange "proof₁")'

def test_make_case():
  assert Commands('./test/test.agda').make_case(0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_make_case 0 noRange "proof₁")'

def test_why_in_scope():
  assert Commands('./test/test.agda').why_in_scope(0, Range(), 'proof₁') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_why_in_scope 0 noRange "proof₁")'

def test_compute():
  assert Commands('./test/test.agda').compute('DefaultCompute', 0, Range(), 'suc (suc zero)') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_compute DefaultCompute 0 noRange "suc (suc zero)")'

def test_why_in_scope_toplevel():
  assert Commands('./test/test.agda').why_in_scope_toplevel('zero') == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_why_in_scope_toplevel "zero")'

def test_show_version():
  assert Commands('./test/test.agda').show_version() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_show_version)'

def test_abort():
  assert Commands('./test/test.agda').abort() == \
    'IOTCM "./test/test.agda" NonInteractive Indirect (Cmd_abort)'

