#!/bin/bash

pushd so1rb 
find -name '*.py' | zip ../so1rb -@
popd

pushd so1rb_explore
find -name '*.py' | zip ../so1rb_explore -@
popd

