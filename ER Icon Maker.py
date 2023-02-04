from pathlib import Path
import os
import glob
import mset

def setTemplateScenePath():
    global templateScenePath
    templateScenePath = mset.showOpenFileDialog(["tbscene"], False)

def setModelsFolder():
    global modelsFolder
    modelsFolder = mset.showOpenFolderDialog()
    
def setTexturesFolder():
    global texturesFolder
    texturesFolder = mset.showOpenFolderDialog()
    
def main():
    textureFilePaths = glob.glob(texturesFolder + "*.png")
    modelFilePaths = glob.glob(modelsFolder + "*.fbx")
    for modelFilePath in modelFilePaths:
        mset.loadScene(templateScenePath)
        rawModelName = Path(modelFilePath).stem
        outputFolder = modelsFolder + "output/" + rawModelName + "/"
        if not os.path.exists(outputFolder): os.makedirs(outputFolder)
        model = mset.importModel(modelFilePath)
        parentMesh = model.getChildren()[0];
        parentMesh.cullBackFaces = False
        model.scale = [-1.0, model.scale[1], model.scale[2]]
        model.rotation = [90, model.rotation[1], model.rotation[2]]
        camera = mset.findObject("Main Camera")
        camera.rotation = [-5.485, 920.1, 0.0]
        mset.frameObject(model)
        baseMaterial = mset.findMaterial("base")
        subMeshes = parentMesh.getChildren()
        for subMesh in subMeshes:
            rawSubMeshName = subMesh.name.replace(".dds", "")
            newMaterial = baseMaterial.duplicate(subMesh.name + "_new")
            for textureFilePath in textureFilePaths:
                if rawSubMeshName[:-2] in textureFilePath:
                    textureType = textureFilePath.replace(".png", "")[-2:]
                    if textureType == "_d":
                        newMaterial.albedo.setField("Albedo Map", textureFilePath)
                    elif textureType == "_n":
                        newMaterial.surface.setField("Normal Map", textureFilePath)
                        newMaterial.microsurface.setField("Roughness Map", textureFilePath)
                    elif textureType == "_m":
                        newMaterial.clearcoatReflectivity.setField("Specular Map", textureFilePath)
            subMesh.material = newMaterial
        subMeshPrefixes = ["HD", "BD", "AM", "LG"]
        prefixOutputNames = ["head", "body", "arms", "legs"]
        cameras = ["ER_Head", "ER_Body", "ER_Arms", "ER_Legs"]
        index = 0
        for subMeshPrefix in subMeshPrefixes:
            for subMesh in subMeshes:
                if subMeshPrefix in subMesh.name and subMesh.name[3:7] == parentMesh.name[3:7]: subMesh.visible = True
                else: subMesh.visible = False
            mset.renderCamera(outputFolder + rawModelName + "_" + prefixOutputNames[index] + ".png", 2048, 2048, 256, True, cameras[index])
            index += 1    
        mset.saveScene(outputFolder + rawModelName + ".tbscene")

iconMakerWindow = mset.UIWindow("ER Icon Maker")
iconMakerWindow.width = iconMakerWindow.width + 150
templateSceneButton = mset.UIButton("Set Template Scene")
templateSceneButton.onClick = setTemplateScenePath
iconMakerWindow.addElement(templateSceneButton)
modelsFolderButton = mset.UIButton("Set Models Folder")
modelsFolderButton.onClick = setModelsFolder
iconMakerWindow.addElement(modelsFolderButton)
texturesFolderButton = mset.UIButton("Set Textures Folder")
texturesFolderButton.onClick = setTexturesFolder
iconMakerWindow.addElement(texturesFolderButton)
goButton = mset.UIButton("Go!")
goButton.onClick = main
iconMakerWindow.addElement(goButton)