oc patch OCSInitialization ocsinit -n openshift-storage --type json --patch  '[{ "op": "replace", "path": "/spec/enableCephTools", "value": true }]'

export TOOLS_POD=$(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name)
echo $TOOLS_POD
oc rsh -n openshift-storage $TOOLS_POD << EOF
ceph status
ceph osd tree
ceph df
EOF

#oc rsh -n openshift-storage $TOOLS_POD ceph status
#oc rsh -n openshift-storage $TOOLS_POD ceph osd tree
#oc rsh -n openshift-storage $TOOLS_POD ceph df
